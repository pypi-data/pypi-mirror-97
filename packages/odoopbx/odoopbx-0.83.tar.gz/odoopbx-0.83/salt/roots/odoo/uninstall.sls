{%- from "odoo/map.jinja" import odoo with context -%}

odoo-stop:
  service.dead:
    - name: odoo
    - enable: False

odoo-remove:
  file.absent:
    - names:
      - /var/lib/odoo
      - /etc/systemd/system/odoo.service
  pkg.removed:
    - name: odoo
