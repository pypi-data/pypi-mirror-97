{%- from "odoo/map.jinja" import odoo with context -%}
{% set version_short = odoo.version.split('.')[0] %}

odoo-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - pip: odoo-addons-reqs

odoo-addons-not-synlink:
  file.directory:
    - name: /srv/odoo/addons/{{ odoo.version }}
    - follow_symlinks: False
    - allow_symlink: False
    - force: False

odoo-addons-cloned:
  git.latest:
    - name: git@gitlab.com:odoopbx/addons.git
    - branch: {{ odoo.version }}
    - depth: 1
    - fetch_tags: False
    - rev: {{ odoo.version }}
    - target: /srv/odoo/addons/{{ odoo.version }}
    - identity: salt://files/id_rsa
    - require:
      - odoo-addons-not-synlink
    - force_checkout: True
    - force_clone: True
    - force_reset: True

odoo-addons-reqs:
  pip.installed:
    - upgrade: {{ odoo.upgrade }}
    - requirements: /srv/odoo/addons/{{ odoo.version }}/requirements.txt
    - bin_env: /srv/odoo/venv/odoo{{ version_short }}
    - require:
      - odoo-addons-cloned
    - retry: True

odoo-addons-init:
  cmd.run:
    - name: >
        /srv/odoo/venv/odoo{{ version_short }}/bin/python /srv/odoo/src/odoo-{{ odoo.version }}/odoo-bin 
        --config /etc/odoo/odoo{{ version_short }}.conf --no-http --stop-after-init  -i asterisk_base_sip,asterisk_calls_crm
    - unless: >
        echo "env['asterisk_base.server']" |
        /srv/odoo/venv/odoo{{ version_short }}/bin/python /srv/odoo/src/odoo-{{ odoo.version }}/odoo-bin  shell
        --config /etc/odoo/odoo{{ version_short }}.conf --no-http
    - require:
      - odoo-addons-reqs
    - runas: {{ odoo.user }}
    - shell: /bin/bash
