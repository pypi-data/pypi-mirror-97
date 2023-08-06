#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from namekox_websocket.core.wsshub import WebSocketHub
from namekox_webserver.core.entrypoints.app.server import WebServer
from namekox_websocket.constants import WEBSOCKET_CONFIG_KEY, DEFAULT_WEBSOCKET_HOST, DEFAULT_WEBSOCKET_PORT


logger = getLogger(__name__)


class WssServer(WebServer):
    def __init__(self, *args, **kwargs):
        self.hub = WebSocketHub()
        super(WssServer, self).__init__(*args, **kwargs)

    def setup(self):
        if self.host is not None and self.port is not None and self.sslargs is not None and self.srvargs is not None:
            return
        config = self.container.config.get(WEBSOCKET_CONFIG_KEY, {}).copy()
        self.middlewares = config.pop('middlewares', []) or []
        self.host = config.pop('host', DEFAULT_WEBSOCKET_HOST) or DEFAULT_WEBSOCKET_HOST
        self.port = config.pop('port', DEFAULT_WEBSOCKET_PORT) or DEFAULT_WEBSOCKET_PORT
        self.sslargs = {k: config.pop(k) for k in config if k in self.SSL_ARGS}
        self.sslargs and self.sslargs.update({'server_side': True})
        self.srvargs = config
