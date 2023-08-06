agent-x509-pki-dir:
  file.directory:
    - name: /etc/odoopbx/pki/selfsigned
    - mode: 0711
    - makedirs: True

agent-x509-private-key:
  x509.private_key_managed:
    - name: /etc/odoopbx/pki/selfsigned/privkey.pem
    - require:
      - agent-x509-pki-dir
    - creates:
      - /etc/odoopbx/pki/selfsigned/privkey.pem

agent-x509-certificate:
  x509.certificate_managed:
    - name: /etc/odoopbx/pki/selfsigned/fullchain.pem
    - signing_private_key: /etc/odoopbx/pki/selfsigned/privkey.pem
    - CN: "{{grains['id']}}"
    - basicConstraints: "critical CA:true"
    - keyUsage: "critical digitalSignature, keyEncipherment"
    - subjectKeyIdentifier: hash
    - authorityKeyIdentifier: keyid,issuer:always
    - days_valid: 3650
    - days_remaining: 0
    - require:
      - agent-x509-private-key
    - creates:
      - /etc/odoopbx/pki/selfsigned/fullchain.pem

agent-x509-symlink:
  file.symlink:
    - name: /etc/odoopbx/pki/current
    - target: /etc/odoopbx/pki/selfsigned
    - creates: /etc/odoopbx/pki/current
