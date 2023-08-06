ipset-add-authenticated:
  caller.cmd.run:
    - args:
        - cmd: >
            ipset add -exist authenticated
            {{ data.RemoteAddress.split('/')[2] }}
            comment "{{ data.get('Service') ~ ' ' ~ data.get('Event') }}
            {{ data.get('AccountID') }}"

ipset-del-expire_long:
  caller.cmd.run:
    - args:
        - cmd: >
            ipset del -exist expire_long {{ data.RemoteAddress.split('/')[2] }}
