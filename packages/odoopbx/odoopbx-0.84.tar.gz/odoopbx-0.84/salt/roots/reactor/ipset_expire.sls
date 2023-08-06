ipset-add-expire_short:
  caller.cmd.run:
    - args:
        - cmd: >
            ipset add -quiet expire_short
            {{ data.RemoteAddress.split('/')[2] }}
            comment "{{ data.get('Service') ~ ' ' ~ data.get('Event') }}
            {{ data.get('AccountID') }}"
        - ignore_retcode: True

ipset-add-expire_long:
  caller.cmd.run:
    - args:
        - cmd: >
            ipset add -exist expire_long
            {{ data.RemoteAddress.split('/')[2] }}
            comment "{{ data.get('Service') ~ ' ' ~ data.get('Event') }}
            {{ data.get('AccountID') }}"
