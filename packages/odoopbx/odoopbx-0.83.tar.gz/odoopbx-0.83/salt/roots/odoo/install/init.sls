{%- from "odoo/map.jinja" import odoo with context -%}

{% set version_short = odoo.version.split('.')[0] %}

include:
  - .server
  - .addons
  - .frontend

{% if grains.virtual != 'container' %}
odoo-service-start:
  service.running:
    - name: odoo{{ version_short }}
    - enable: true
    - require:
      - cmd: odoo-addons-init
{% endif %}
