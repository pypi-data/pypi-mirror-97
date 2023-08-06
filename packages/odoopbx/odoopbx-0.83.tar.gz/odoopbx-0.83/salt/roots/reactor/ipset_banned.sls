ipset-add-banned:
  caller.cmd.run:
    - args:
        - cmd: >
            ipset add -exist banned {{ data.RemoteAddress.split('/')[2] }}
            comment "{{ data.get('Service') ~ ' ' ~ data.get('Event') }}
            {{ data.get('AccountID') }}"

log-banned:
  caller.log.warning:
    - args:
        - message: >
            IP {{ data.RemoteAddress.split('/')[2] }} banned.
            {{ data.get('Service') ~ ' ' ~ data.get('Event') }}
            {{ data.get('AccountID') }}

ipset-del-expire_long:
  caller.cmd.run:
    - args:
        - cmd: >
            ipset del -exist expire_long {{ data.RemoteAddress.split('/')[2] }}
