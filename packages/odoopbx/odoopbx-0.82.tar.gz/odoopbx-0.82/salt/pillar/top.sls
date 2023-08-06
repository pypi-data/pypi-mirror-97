{% set pillar_path_0 = salt['config.get']('pillar_roots')[saltenv][0] -%}
{{ saltenv }}:
  '*':
    - odoopbx
    {%- if salt['file.file_exists']( pillar_path_0 ~ '/id/' ~ grains.machine_id ~ '.sls') %}
    - id/{{ grains.machine_id }}
    {%- endif %}
  'G@virtual:container':
    - virtual-container
