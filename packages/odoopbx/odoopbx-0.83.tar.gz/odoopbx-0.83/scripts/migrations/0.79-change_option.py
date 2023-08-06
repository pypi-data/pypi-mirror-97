import yaml
import os


def migrate():
    SALT_PATH = '/etc/odoopbx'
    config_path = os.path.join(SALT_PATH, 'local.conf')
    config = yaml.load(open(config_path), yaml.SafeLoader)
    if config.get('connector_listen_port'):
        config['connector_port'] = config['connector_listen_port']
        del config['connector_listen_port']
    open(config_path, 'w').write(
        yaml.dump(config, default_flow_style=False, indent=2))
    print('Done.')
