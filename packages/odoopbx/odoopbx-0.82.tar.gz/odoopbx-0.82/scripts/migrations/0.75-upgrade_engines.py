import yaml
import os


def migrate():
    SALT_PATH = '/etc/odoopbx'
    config_path = os.path.join(SALT_PATH, 'local.conf')
    config = yaml.load(open(config_path), yaml.SafeLoader)
    # Odoo connector
    engines = config.get('engines', [])
    if engines:
        del config['engines']
    for engine in engines:
        if isinstance(engine, dict) and engine.get('odoo_connector'):
            print('odoo_connector' in engine, engine['odoo_connector'])
            odoo_connector = engine['odoo_connector']
            config['connector_bus_enabled'] = odoo_connector.get('bus_enabled')
            config['connector_http_enabled'] = odoo_connector.get('http_enabled')
            config['connector_listen_port'] = odoo_connector.get('http_listen_port')
            config['agent_listen_address'] = odoo_connector.get('http_listen_address')
        elif isinstance(engine, dict) and engine.get('asterisk_cli'):
            asterisk_cli = engine['asterisk_cli']
            config['asterisk_cli_port'] = asterisk_cli.get('listen_port')
            config['asterisk_binary'] = asterisk_cli.get('asterisk_binary')
            config['asterisk_options'] = asterisk_cli.get('asterisk_options')
    config['engines'] = [
        'reactor',
        'asterisk_ami',
        'odoo_connector',
        'asterisk_cli'
    ]
    open(config_path, 'w').write(
        yaml.dump(config, default_flow_style=False, indent=2))
    print('Done.')
