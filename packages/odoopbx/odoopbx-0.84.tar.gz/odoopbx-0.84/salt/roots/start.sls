asterisk_agent_start:
  module.run:
    - odoo.execute:
      - model: asterisk_common.settings
      - method: on_agent_start
      - args: []
