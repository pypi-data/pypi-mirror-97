{% from "agent/map.jinja" import agent with context %}

{% if grains.os_family == 'RedHat' %}
agent-pkg-reqs-RedHat:
  pkg.installed:
    - names:
      - epel-release
{% endif %}

agent-pkg-reqs:
  pkg.installed:
    - pkgs: {{ agent.pkgs }}
    - refresh: true

agent-pip-reqs:
  pip.installed:
    - pkgs:
      - jsonrpcserver
      - aiorun
      - ipsetpy
      - odoopbx
      - OdooRPC
      - https://github.com/litnimax/panoramisk/archive/master.zip
      - pastebin
      - setproctitle
      - terminado
      - tornado-httpclient-session
    - require:
      - agent-pkg-reqs
    - retry: True
    - reload_modules: True

agent-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - agent-pip-reqs

agent-locale:
  locale.present:
    - name: C.UTF-8

agent-service-file:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
    - template: jinja

agent-grains-update:
  grains.present:
    - name: letsencrypt:domainsets:odoopbx
    - value:
        - '{{ salt['config.get']('fqdn') }}'
    - force: True

{% if grains.get('virtual') != "container" and grains.get('virtual_subtype') != "Docker" %}
agent-service-enable:
  service.enabled:
    - name: odoopbx-agent
    - require:
      - agent-pip-reqs
      - agent-service-file
{% endif %}
