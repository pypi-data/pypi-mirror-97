postgres:
  bake_image: True
nginx:
  service:
    opts:
      onlyif:
        - runlevel
