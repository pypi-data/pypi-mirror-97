include:
  - ..letsencrypt

letsencrypt-activate-cert:
  file.symlink:
    - onlyif:
        fun: x509.read_certificate
        certificate: /etc/letsencrypt/live/odoopbx/cert.pem
    - name: /etc/odoopbx/pki/current
    - target: /etc/letsencrypt/live/odoopbx
