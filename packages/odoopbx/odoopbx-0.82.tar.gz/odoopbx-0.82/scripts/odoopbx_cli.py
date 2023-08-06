import click
from datetime import datetime, timedelta
import json
import importlib.util
import logging
import os
import requests
import signal
import sys
import shutil
import subprocess
import tempfile
import time
import uuid
import yaml
import odoopbx
import odoopbx.scripts

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

SALT_PATH = '/etc/odoopbx'

STARS = '*' * 20
MASTER_CONF = {
    'master': 'master.odoopbx.com:44506',
    'master_type': 'str',
    'publish_port': 44505,
    'use_master_when_local': True,
    'master_tries': -1,
    'master_alive_interval': 10,
    'auth_tries': -1,
    'ping_interval': 1, # minutes
    'recon_randomize': False,
    'rejected_retry': True,
    'file_client': 'remote',
}

SUPPORT_LOG_CONF = {
    'logstash_udp_handler': {
        'host': 'log.odoopbx.com',
        'port': 45044,
        'version': 1,
        'msg_type': 'logstash'
    }
}

REACTOR_CONF = {
    'reactor': [{'AMI/*': 'salt://reactor/ami_events.sls'}]
}

def _update_salt_files():
    # Copy salt files and folders from package directory.
    click.echo('Updating salt files...')
    mydir = os.path.dirname(os.path.abspath(__file__))
    salt_dir = os.path.join(mydir, '..', 'salt')
    # Copy folders
    for f in [
            'extensions',
            'minion.d',
            'pillar',
            'roots',
            ]:
        target = os.path.join(SALT_PATH, f)
        # Remove old version
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(os.path.join(salt_dir, f), target)
    # Copy/overwrite files
    for f in ['minion', 'Saltfile']:
        open(os.path.join(SALT_PATH, f), 'w').write(
            open(os.path.join(salt_dir, f)).read())
    # Put a .salted file so that we do not copy on every start.    
    open(os.path.join(SALT_PATH, '.salted'), 'w').write(
        odoopbx.scripts.__version__)


def _install_salt_files():
    if not os.path.exists(SALT_PATH):
        os.mkdir(SALT_PATH)
    _update_salt_files()
    # Check for flag to update salt files
    salted_file = os.path.join(SALT_PATH, '.salted')
    if not os.path.exists(salted_file):
        _update_salt_files()
    elif open(salted_file).read() != odoopbx.scripts.__version__:
        _update_salt_files()
    if not os.path.exists(os.path.join(SALT_PATH, 'local.conf')):
        custom_conf = open(os.path.join(SALT_PATH, 'local.conf'), 'w')
        custom_conf.write('# Custom options.\n\nid: {}\n'.format(
            str(uuid.getnode())))
        if not os.path.exists('/dev/log'):
            custom_conf.write('log_file: /var/log/odoopbx.log\n')
        custom_conf.close()


@click.group()
def main():
    # Set the locale.
    if 'utf' not in os.getenv('LANG', '').lower():
        os.environ['LANG'] = os.environ['LC_ALL'] = 'C.UTF-8'
    # Check for /etc/odoopbx folder
    if not os.path.exists(os.path.join(SALT_PATH, '.salted')):
        _install_salt_files()
    # Change working folder to Odoo PBX Salt package.
    os.chdir(SALT_PATH)


@main.command(help='Call a command.')
@click.argument('cmd', nargs=-1)
def call(cmd):
    """
    Execute a salt-call command passing all parameters.
    To pass an option use -- e.g. odoopbx call -- --version
    """
    cmd_l = ['salt-call']
    cmd_l.extend(list(cmd))
    os.execvp('salt-call', cmd_l)


@main.group(help='Configuration management.')
def config():
    pass


def _config_load():
    config_path = os.path.join(SALT_PATH, 'local.conf')
    config = yaml.load(open(config_path), yaml.SafeLoader)
    return config


def _config_save(config):
    config_path = os.path.join(SALT_PATH, 'local.conf')
    open(config_path, 'w').write(
        yaml.dump(config, default_flow_style=False, indent=2))


@config.command(name='get')
@click.argument('option')
@click.option('--local', is_flag=True,
              help='Fetch the value directly from .conf file instead '
                   'of internal storage.')
def config_get(option, local):
    """
    Get a configuration option's value.
    """
    if not local:
        os.execvp('odoopbx', ['odoopbx', 'call', 'config.get', option])
    else:
        config = _config_load()
        if option not in config:
            click.secho('Option {} not found'.format(option), fg='red')
        else:
            click.echo('Value of type: {}.\n\n{}'.format(
                type(config[option]).__name__,
                yaml.dump(config[option], default_flow_style=False, indent=2)))


@config.command(name='set')
@click.argument('option')
@click.argument('value')
def config_set(option, value):
    """
    Set a configuration option passed as JSON.

    Examples:

        odoopbx config set ami_trace_actions true # true and not True
        odoopbx config set ami_trace_events '["Cdr","FullyBooted"]'

    You can verify how option value is treated by calling:

        odoopbx config get --raw ami_trace_events
    """
    try:
        value = json.loads(value)
    except json.decoder.JSONDecodeError:
        # String value
        pass
    config = _config_load()
    if option not in config:
        click.secho('Option {} not found, creating a new one.'.format(
                    option), fg='red')
    config[option] = value
    _config_save(config)


@config.command(name='del')
@click.argument('option')
def config_del(option):
    config = _config_load()
    if option not in config:
        click.secho('Option {} not found, nothing to delete.'.format(
                    option), fg='red')
        return
    del config[option]
    _config_save(config)


@main.group(help='Run service.',
            invoke_without_command=True)
@click.argument('service', nargs=-1, required=True)
def run(service):
    service = list(service)
    if 'agent' in service:
        service.remove('agent')
        service.insert(0, 'salt-minion')
        os.execvp('salt-minion', service)
    else:
        click.echo('Not yet implemented')


@main.command(help='Enable a service.')
@click.argument('service', required=True)
def enable(service):
    # Firewall
    if service == 'reactor':
        config = _config_load()
        config.update(REACTOR_CONF)
        _config_save(config)
    else:
        os.execvp('systemctl', ['systemctl', 'enable', service])


@main.command(help='Disable a service.')
@click.argument('service', required=True)
def disable(service):
    # Firewall
    if service == 'reactor':
        config = _config_load()
        config['reactor'] = []
        _config_save(config)
    else:
        if service == 'agent':
            service = 'odoopbx-agent'
        os.execvp('systemctl', ['systemctl', 'disable', service])


@main.command(help='Install a service / all services')
@click.argument('service')
def install(service):
    if service == 'all':
        os.execvp('salt-call', ['salt-call', '-l', 'info', 'state.highstate'])
    else:
        os.execvp('salt-call', ['salt-call', '-l', 'info', 'state.apply', service])


@main.command(help='Restart a service')
@click.argument('service')
def restart(service):
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'restart', service])


@main.command(help='Start a service.')
@click.argument('service')
def start(service):
    # Little magic to save time.
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'start', service])


@main.command(help='Stop a service.')
@click.argument('service')
@click.option('--kill', is_flag=True)
def stop(service, kill):
    # Little magic to save time.
    if service == 'agent':
        service = 'odoopbx-agent'
    subprocess.check_output('systemctl stop {}'.format(service), shell=True)
    if kill:
        # Works only for agent
        if service != 'odoopbx-agent':
            click.secho('Only Agent kill is currently supported')
            return
        def _get_pids():
            pids = subprocess.check_output(
                "ps -ef | grep -v grep | grep minion | awk '{print $2}'",
                shell=True).decode()
            if pids:
                pids = [int(k) for k in pids.split('\n') if k]
            else:
                pids = []
            return pids
        pids = _get_pids()
        if pids:            
            for pid in pids:
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            click.echo('Killed {} processes.'.format(len(pids)))    
        else:
            click.echo('No processes to kill.')


@main.group(help='Show information.')
def show():
    pass


@show.command(help='Show system version.', name='version')
def show_version():    
    click.echo('Odoo PBX ID: {} CLI version: {}.'.format(
        _config_load()['id'], odoopbx.scripts.__version__))


@show.command(help='Show system status.', name='report')
def show_report():
    # Print LISTENING ports
    click.secho('{} NETWORK PORTS {}'.format(STARS, STARS), bold=True)
    os.system('netstat -atnup | grep LISTEN')
    # Print running python processes
    click.secho('{} PYTHON PROCS {}'.format(STARS, STARS), bold=True)
    os.system('ps auxw | grep python')


@main.group(help='Technical support')
def support():
    pass

@support.command(name='on',
                 help='Connect the Agent to remote support.')
def support_on():
    config = _config_load()
    config.update(MASTER_CONF)
    _config_save(config)
    click.echo(
        'Your Agent ID: {}. Tell this ID to the tech support officer.'.format(
            config['id']))
    click.echo('Support configuration enabled. Restart the Agent to apply.')


@support.command(name='off',
                 help='Disconnect the Agent from remote support.')
def support_off():
    config = _config_load()
    options = MASTER_CONF.keys()
    for option in options:
        if option in config:
            del config[option]
    _config_save(config)
    click.echo('Support configuration disabled. Restart the Agent to apply.')


@support.command(name='status',
                 help='Show the current status of remote support.')
def support_status():
    config = _config_load()
    status = subprocess.check_output(
        'odoopbx config get master_type', shell=True).decode()
    if 'disable' in status:
        click.echo('Remote support configuration is off.')
    else:
        click.echo('Remote support configuration is on')


@support.command(name='start',
                 help='Start the OdooPBX agent in support only mode.')
def support_start():
    config = _config_load()
    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            conf = ['{}: {}'.format(k, v) for k,v in MASTER_CONF.items()]
            conf.extend([
                'id: {}'.format(config['id']),
                'root_dir: {}'.format(tmpdirname),
            ])
            open(os.path.join(tmpdirname, 'minion'),
                 'w').write('\n'.join(conf))
            os.chdir(tmpdirname)
            print(tmpdirname)
            # Try to copy PKIs
            if os.path.isdir(os.path.join(SALT_PATH, 'pki')):
                shutil.copytree(
                    os.path.join(SALT_PATH, 'pki'),
                    os.path.join(tmpdirname, 'etc', 'salt', 'pki'))
            click.echo(
                'Support session for ID {} is started.'.format(config['id']))
            click.echo(
                'When support session is over type CTRL+C to terminate it...')
            subprocess.check_output('salt-minion -c {}'.format(tmpdirname),
                                    shell=True)
        except KeyboardInterrupt:
            click.echo('Stopping...')
            time.sleep(3)
            click.echo('Stopped.')

@support.command(name='report')
def support_report():
    report = ''
    # Add config
    config = _config_load()
    report += '{}\n\n\n'.format(json.dumps(config, indent=2))
    from pastebin import PastebinAPI
    import urllib
    api_url = 'http://pastebin.com/api/api_post.php'
    api_dev_key = 'f3e3abf8f670086901d809c5053b1e78'
    data = {
        'api_dev_key': api_dev_key,
        'api_user_key': '',
        'api_option': 'paste',
        'api_paste_format': 'bash',
        'api_paste_code': report,
        'api_paste_name': uuid.uuid4().hex,
        'api_paste_private': '1',
        'api_paste_expire_date': '10M',
    }
    request_string = urllib.request.urlopen(
        api_url, urllib.parse.urlencode(data).encode("utf-8"))
    click.echo('Send this link to the tech support:')
    click.echo(request_string.read())
    click.echo('This report will be automatically destroyed in 10 minutes...')


@support.group(help='Configure sending the Agent logs to the support.')
def logger():
    pass


@logger.command(name='on', help='Enable sending logs to the support.')
def logger_on():
    config = _config_load()
    config.update(SUPPORT_LOG_CONF)
    _config_save(config)
    click.echo('Support logger is enabled. Please restart the Agent.')


@logger.command(name='off', help='Disable sending logs to the support.')
def logger_off():
    config = _config_load()
    if 'logstash_udp_handler' in config:
        del config['logstash_udp_handler']
        _config_save(config)
        click.echo('Support logger is disabled. Please restart the Agent.')
    else:
        click.echo('Support logger was not enabled.')


@main.group(help='Upgrade Odoo PBX')
def upgrade():
    pass


def _migrate():
    mydir = os.path.dirname(os.path.abspath(__file__))
    migrations_dir = os.path.join(mydir, 'migrations')
    current_ver = float(open(os.path.join(SALT_PATH, '.salted')).read())
    latest_ver = float(odoopbx.scripts.__version__)
    files = [k for k in os.listdir(migrations_dir) if k.endswith('.py')]
    files.sort()
    for f in files:
        try:
            script_ver = float(f.split('-')[0])
        except ValueError:
            continue
        if script_ver > current_ver and script_ver < latest_ver:
            click.echo('Doing migration for {}... '.format(script_ver),
                       nl=False)
            pyfile = os.path.join(migrations_dir, f)
            spec = importlib.util.spec_from_file_location('migrate', pyfile)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.migrate()


@upgrade.command(help='Upgrade the Agent', name='agent')
def upgrade_agent():
    _migrate()
    _update_salt_files()


if __name__ == '__main__':
    main()
