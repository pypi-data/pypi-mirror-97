"""
Engine that recieves salt commands from Odoo bus.
"""
from __future__ import absolute_import, print_function, unicode_literals
import concurrent.futures
from functools import partial
from httpclient_session import Session
from jsonrpcserver import method, dispatch as dispatch
import logging
import os
import pwd
import resource
import salt.utils.event
from salt.utils import json
import salt.utils.process
from salt.ext.tornado.locks import Event
from salt.ext.tornado import ioloop
from salt.ext.tornado.web import Application
from salt.ext.tornado.httpserver import HTTPServer
from salt.ext.tornado.httpclient import AsyncHTTPClient, HTTPRequest
from salt.ext.tornado.web import RequestHandler
from salt.ext.tornado.gen import sleep, coroutine
import sys
import time
import uuid
import odoopbx.scripts


log = logging.getLogger(__name__)
logging.getLogger('jsonrpcserver').setLevel(logging.WARNING)

__virtualname__ = 'odoo_connector'

CHANNEL_PREFIX = 'remote_agent'

VERSION = odoopbx.scripts.__version__


def __virtual__():
    return __virtualname__


def start():
    log.info('Starting Odoo bus engine...')
    OdooConnector().start()


@method
def execute(method, args, kwargs):
    log.debug('Method: %s, args: %s, kwargs: %s', method, args, kwargs)
    callback = kwargs.pop('callback', [])
    passback = kwargs.pop('passback', {})
    status_notify_uid = kwargs.pop('status_notify_uid', False)
    delay = float(kwargs.pop('delay', False))
    if delay:
        # Delay the method execution
        log.debug('Delaying method %s execution for %s...', method, delay)
        time.sleep(delay)
    try:
        # Run the mothod.
        res = __salt__[method](*args, **kwargs)
        if status_notify_uid:
            # Notify about method call status
            status = 'Success' if bool(res) else 'Failed'
            log.debug('Notify UID %d status: %s', status_notify_uid, bool(res))
            try:
                __salt__['odoo.notify_user'](status_notify_uid, status,
                                             title=method)
            except Exception as e:
                log.exception('Method %s status notify error:', method)
        if callback:
            # Run the callback to pass mwthod results.
            log.debug('Execute %s.%s.', callback[0], callback[1])
            try:
                __salt__['odoo.execute'](callback[0], callback[1], [{
                    'result': res,
                    'passback': passback,
                    }]
                )
            except Exception as e:
                log.exception('Callback %s error:', callback)
        return res
    # Method error.
    except Exception as e:
        if callback:
            try:
                __salt__['odoo.execute'](
                    callback[0], callback[1], [{
                        'error': {'message': str(e)},
                        'passback': passback
                    }]
                )
            except Exception as e:
                log.exception('Callback %s error:', callback)
        if status_notify_uid:
            # Notify about method call status
            status = 'Error'
            try:
                __salt__['odoo.notify_user'](status_notify_uid, status,
                                             title=method)
            except Exception as e:
                log.exception('Method %s status notify error:', method)
        # And raise it again.
        raise


class OdooConnector:
    db_selected = False
    http_session = None  # Requests session for bus polling
    db_selected = False
    # Init token
    token = old_token = None
    token_update_time = time.time()
    # Default timeout
    bus_timeout = 60
    refresh_token_seconds = 300
    # Update on start before making first ping.
    token_updated = Event()

    def __init__(self):
        self.listen_address = __salt__['config.get']('agent_listen_address')
        self.listen_port = __salt__['config.get']('connector_port')
        self.http_enabled = __salt__['config.get']('connector_http_enabled')
        self.bus_enabled = __salt__['config.get']('connector_bus_enabled')

    def start(self):
        # Set some options
        salt.utils.process.appendproctitle(self.__class__.__name__)
        resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 16384))
        self.bus_timeout = int(
            __salt__['config.get']('odoo_bus_timeout', 60))
        self.refresh_token_seconds = float(__salt__['config.get'](
            'odoo_refresh_token_seconds', 300))
        self.trace_rpc = __salt__['config.get']('odoo_trace_rpc')
        # Handle request executor
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        # Start workers
        self.io_loop = ioloop.IOLoop(make_current=False)
        self.io_loop.make_current()
        self.io_loop.spawn_callback(self.poll_bus)
        self.io_loop.spawn_callback(self.update_token)
        self.io_loop.spawn_callback(self.listen_http)
        self.http_session = Session()
        self.io_loop.start()

    async def select_db(self):
        """
        For multi database Odoo setup it is required to first select a database
        to work with. But if you have single db setup or use db_filters
        so that always one db is selected set odoo_single_db=True in settings.
        """
        if self.db_selected:
            return
        log.info('Selecting Odoo database (session refresh)')
        scheme = 'https' if __salt__['config.get']('odoo_use_ssl') else 'http'
        auth_url = '{}://{}:{}/web/session/authenticate'.format(
            scheme, __salt__['config.get']('odoo_host', 'localhost'),
            int(__salt__['config.get']('odoo_bus_port', 8072)))
        log.debug('Odoo authenticate at %s', auth_url)
        data = {
            'jsonrpc': '2.0',
            'params': {
                'context': {},
                'db': __salt__['config.get']('odoo_db', 'demo'),
                'login': __salt__['config.get']('odoo_user', 'admin'),
                'password': __salt__['config.get']('odoo_password'),
            },
        }
        headers = {
            'Content-type': 'application/json'
        }
        req = HTTPRequest(auth_url, method='POST', body=json.dumps(data),
                          headers=headers)
        rep = await self.http_session.fetch(req)
        result = json.loads(rep.body)
        if rep.code != 200 or result.get('error'):
            log.error(u'Odoo authenticate error {}: {}'.format(
                rep.code,
                json.dumps(result['error'], indent=2)))
        else:
            log.info('Odoo authenticated for long polling.')
        self.db_selected = True

    def send_bus_ping(self):
        __salt__['odoo.execute'](
            'remote_agent.agent', 'bus_sendone',
            ['remote_agent/{}'.format(__grains__['id']),
             {'command': 'bus_ping'}])

    def set_agent_system_name(self):
        # This sets agent's system name for remote connection.
        __salt__['odoo.execute']('remote_agent.agent', 'update_system_name',
            [__grains__['id'], VERSION])

    async def poll_bus(self):
        """
        Odoo bus poller to get massages from Odoo
        and convert it in Salt job.
        """
        # Update Agent's system name
        self.set_agent_system_name()
        # Wait for the new token.
        if not self.bus_enabled:
            log.debug('Odoo bus not enabled.')
            return
        await self.token_updated.wait()
        # Send the first ping message that will be omitted.
        self.send_bus_ping()
        # Init the message pointer.
        last = 0
        scheme = 'https' if __salt__['config.get']('odoo_use_ssl') else 'http'
        odoo_host = __salt__['config.get']('odoo_host', 'localhost')
        bus_port = int(__salt__['config.get']('odoo_bus_port', 8072))
        single_db = __salt__['config.get']('odoo_single_db')
        minion_id = __grains__['id']
        while True:
            try:
                bus_url = '{}://{}:{}/longpolling/poll'.format(
                    scheme, odoo_host, bus_port)
                # Select DB first
                if not single_db:
                    await self.select_db()
                # Now let try to poll
                log.info('Polling %s.', bus_url)
                req = HTTPRequest(
                    bus_url,
                    method='POST',
                    body=json.dumps({'params': {
                        'last': last,
                        'channels': ['{}/{}'.format(
                            CHANNEL_PREFIX, minion_id)]}}),
                    headers={'Content-Type': 'application/json'},
                    request_timeout=self.bus_timeout)
                r = await self.http_session.fetch(req)
                try:
                    json.loads(r.body)
                except ValueError:
                    log.error('JSON parse bus reply error: %s', r.body)
                result = json.loads(r.body).get('result')
                if not result:
                    error = json.loads(r.body).get(
                        'error', {}).get('data', {}).get('message')
                    if error:
                        log.error('Odoo bus error: %s', error)
                        # Sleep 1 sec not to flood the log.
                        await sleep(1)
                        continue
                if last == 0:
                    # Ommit queued data
                    for msg in result:
                        log.debug('Ommit bus message %s', str(msg)[:512])
                        last = msg['id']
                    continue
                # TODO: Check that tis is really
                # my channel as Odoo can send a match
                for msg in result:
                    last = msg['id']
                    log.debug('Received bus message %s', str(msg)[:512])
                    try:
                        f = partial(
                            self.handle_message_async,
                            msg['channel'], msg['message'])
                        self.io_loop.spawn_callback(f)
                    except Exception:
                        log.exception('Handle bus message error:')

            except Exception as e:
                no_wait = False
                if 'Connection refused' in str(e):
                    log.warning('Odoo Connection refused.')
                elif 'Stream closed' in str(e):
                    log.warning('Odoo Connection closed.')
                elif 'Internal Server Error' in str(e):
                    log.warning('Odoo Internal Server Error')
                elif 'Timeout' in str(e):
                    # Do not wait on reconnect on notmal timeouts.
                    no_wait = True
                    log.info('Bus poll timeout, re-polling.')
                elif 'Cannot assign requested address' in str(e):
                    log.warning('Odoo connection lost.')
                else:
                    log.exception('Bus error:')
                if not no_wait:
                    await sleep(1)

    async def handle_message_async(self, channel, message):
        @coroutine
        def blocking_call():
            f = partial(self.handle_message, channel, message)
            future = self.executor.submit(f)
            return (yield future)
        return await blocking_call()

    def handle_message(self, channel, raw_message):
        # Check message type
        try:
            message = raw_message if isinstance(
                raw_message, dict) else json.loads(raw_message)
        except TypeError:
            log.error('Cannot load json from message: %s', raw_message)
            return
        if message.get('command') == 'bus_ping':
            logger.debug('Bus ping received.')
            return
        # Check for security token
        if not self.check_security_token(message.get('token')):
            log.error('Loosing message, bad message token: %s', message)
            self.io_loop.spawn_callback(self.update_token)
            return
        # Check the destination
        if message.get('system_name') != __opts__['id']:
            log.error('Ignoring message for bad ID: %s',
                      message.get('system_name'))
            return
        # JSON-RPC call
        if message.get('command') == 'jsonrpc':
            if self.trace_rpc:
                log.info('Request: %s', message['request'])
            response = dispatch(message['request'])
            if self.trace_rpc:
                log.info('Response: %s', str(response))
            if message.get('reply_channel'):
                __salt__['odoo.execute'](
                    'asterisk_common.settings', 'bus_sendone',
                    [message.get('reply_channel'), str(response)])
            return response
        # Restart
        elif message.get('command') == 'restart':
            log.info('Restart command received. Restarting')
            # Overwrite the last command not to get it again.
            self.send_bus_ping()
            # Notify user
            uid = message.get('notify_uid')
            if uid:
                try:
                    __salt__['odoo.notify_user'](uid, 'Restarting...')
                except Exception:
                    log.exception('Restart notify error.')
            # Restart
            __salt__['cmd.run']('systemctl restart odoopbx-agent')
        # Uknown command?
        else:
            logger.error('Unknown command: %s', message)

    def check_security_token(self, token):
        if self.token == token:
            return True
        elif self.token != token:
            # Check for race condition when token has been just updated
            if self.old_token == token:
                if abs(time.time() - self.token_update_time) > 3:
                    log.error('Outdated token, ignoring message: %s', token)
                    return False
                else:
                    log.info('Accepting old token message: %s', token)
                    return True
            else:
                log.error('Bad message token: %s', token)
                return False

    async def update_token(self):
        log.debug('Odoo bus token updater started every %s seconds.',
                  self.refresh_token_seconds)
        while True:
            try:                
                new_token = uuid.uuid4().hex                
                if not __salt__.get('odoo.execute'):
                    log.error("__salt__['odoo.execute'] is not available!")
                    await sleep(self.refresh_token_seconds)
                    continue
                __salt__['odoo.execute'](
                    'remote_agent.agent', 'update_token', [new_token])
                log.debug('Odoo token updated.')
                __pillar__['odoo_token'] = new_token
                if not self.token_updated.is_set():
                    self.token_updated.set()
                # Keep previous token
                self.old_token = self.token
                # Generate new token
                self.token = new_token
                # Keep time of token update
                self.token_update_time = time.time()
            except Exception:
                log.exception('Update token error:')
                # Prevent flood
                await sleep(1)
            finally:
                await sleep(self.refresh_token_seconds)

    async def listen_http(self):
        parent = self

        class WebHook(RequestHandler):
            # Copied from Salt engines webhook.
            async def post(self, tag):
                body = self.request.body
                headers = self.request.headers if isinstance(
                    self.request.headers, dict) else dict(self.request.headers)
                json_body = json.loads(body)
                json_body['token'] = headers.get('X-Token')
                response_expected = headers.get('Response-Expected')
                if response_expected == '0':
                    # No response is expected, spawn the method and return
                    f = partial(parent.handle_message_async,
                                tag, json_body)
                    parent.io_loop.spawn_callback(f)
                else:
                    response = await parent.handle_message_async(
                        tag, json_body)
                    self.write(str(response))

        # Is it enabled?
        if not (self.http_enabled and self.listen_port
                and self.listen_address):
            log.info('Incoming Odoo HTTPS listener is not enabled.')
            return
        application = Application([(r"/(.*)", WebHook)])
        ssl_options = False
        ssl_crt = __salt__['config.get']('agent_ssl_crt')
        ssl_key = __salt__['config.get']('agent_ssl_key')
        if all([ssl_crt, ssl_key]):
            ssl_options =  {
                'certfile': ssl_crt,
                'keyfile': ssl_key,
            }
            log.info(
                'Odoo HTTPS connector running at %s:%s',
                self.listen_address, self.listen_port)
        else:
            log.info(
                'Odoo HTTP (not secure) connector running at %s:%s',
                self.listen_address, self.listen_port)
        http_server = HTTPServer(application, ssl_options=ssl_options)
        http_server.listen(self.listen_port,
                           address=self.listen_address)
