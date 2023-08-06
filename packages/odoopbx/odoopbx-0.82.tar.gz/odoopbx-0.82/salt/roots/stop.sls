{%- from "odoo/map.jinja" import odoo with context -%}

stop-services:
  service.dead:
    - names:
      - {{ odoo.odoover }}
      - asterisk
      - postgresql
