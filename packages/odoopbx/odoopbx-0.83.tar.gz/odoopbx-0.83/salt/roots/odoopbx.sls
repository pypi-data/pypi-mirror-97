{% if grains.os_family == "Debian" %}
include:
  - agent
  - asterisk
  - postgres
  - odoo
  - nginx
{% else %}
not-yet-supported:
  test.show_notification:
    - text: Sorry, {{ grains.os_family }} is not supported yet
{% endif %}
