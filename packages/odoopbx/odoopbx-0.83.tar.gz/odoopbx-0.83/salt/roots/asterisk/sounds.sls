# -*- coding: utf-8 -*-
# vim: ft=sls
---

{%- set tplroot = tpldir.split('/')[0] %}
{%- from tplroot ~ "/map.jinja" import asterisk with context %}

{% for sounds in asterisk.sounds %}
{{ 'asterisk-sounds-' ~ sounds.url }}:
  archive.extracted:
    - name: /var/lib/asterisk/sounds/{{ sounds.subdir }}
    - source: {{ sounds.url }}
    - skip_verify: true
    - enforce_toplevel: false
    - user: {{ asterisk.user }}
    - trim_output: 5
{% endfor %}
