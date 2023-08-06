security_ports_udp: 5060,65060
security_ports_tcp: 80,443,5038,5039,5060,5061,65060,8088,8089
odoo_db: odoopbx_13
asterisk:
  lookup:
    rev: certified/16.8

letsencrypt:
  use_package: true
  config:
    #server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: webmaster@odoopbx.com
    authenticator: webroot
    webroot-path: /var/spool/letsencrypt

nginx:
  install_from_repo: true
  package:
    opts: {}
  snippets:
    letsencrypt.conf:
      - location ^~ /.well-known/acme-challenge/:
          - root: /var/spool/letsencrypt
          - default_type: "text/plain"
    proxy_params.conf:
      - proxy_set_header: X-Forwarded-Host $host
      - proxy_set_header: X-Forwarded-For $proxy_add_x_forwarded_for
      - proxy_set_header: X-Forwarded-Proto $scheme
      - proxy_set_header: X-Real-IP $remote_addr
      - proxy_http_version: 1.1
      - proxy_set_header: Upgrade $http_upgrade
      - proxy_set_header: Connection "upgrade"
    auth.conf:
      - satisfy: any
      - allow: 127.0.0.1
      # Uncomment the following to restrict access
      # - deny: all
      # - auth_basic: Restircted
      # - auth_basic_user_file: /etc/nginx/.htpasswd
      # You may use 'htpasswd -c /etc/nginx/.htpasswd admin' from apache2-utils

  server:
    opts: {}
    config:
      worker_processes: 1
      events:
        worker_connections: 128
      http:
        sendfile: 'on'
        server_tokens: 'off'
        gzip: 'on'
        server_names_hash_bucket_size: 64
  servers:
    purge_servers_config: False
    managed:
      odoopbx.conf:
        enabled: true
        config:
          - server:
              - server_name: localhost
              - listen:
                  - '443 ssl'
              - ssl_certificate: /etc/odoopbx/pki/current/fullchain.pem
              - ssl_certificate_key: /etc/odoopbx/pki/current/privkey.pem
              - include:
                  - 'snippets/proxy_params.conf'
              - location /:
                  - proxy_pass: http://localhost:8069
                  - include:
                      - 'snippets/auth.conf'
              - location /longpolling:
                  - proxy_pass: http://localhost:8072
                  - include:
                      - 'snippets/auth.conf'
              - location /ws:
                  - proxy_pass: http://localhost:8088/ws
      default.conf:
        enabled: true
        config:
          - server:
              - server_name: localhost
              - listen:
                  - '80 default_server'
              - include:
                  - 'snippets/letsencrypt.conf'

