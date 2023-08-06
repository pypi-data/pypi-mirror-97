# Install
```shell script
pip install -U namekox-websocket
```

# Example
> ping.py
```python
#! -*- coding: utf-8 -*-

# author: forcemain@163.com
from __future__ import unicode_literals


from namekox_websocket.core.message import WssMessage
from namekox_websocket.core.wsshub import WebSocketHub
from namekox_websocket.core.entrypoints.app.handler import WebSocketHandler
from namekox_webserver.core.entrypoints.app.handler import ApiServerHandler


app = type(__name__, (object,), {'api': ApiServerHandler.decorator, 'wss': WebSocketHandler.decorator})


class Ping(object):
    name = 'ping'
    websocket_hub = WebSocketHub()

    @app.api('/', methods=['GET'])
    def api_pong(self, request):
        message = WssMessage(data={'api_pong': True})
        self.websocket_hub.broadcast('ping', message)

    @app.wss('/', methods=['GET'])
    def wss_pong(self, request, sock_id, data):
        self.websocket_hub.subscribe('ping', sock_id)
        return {'wss_pong': True}
```

# Running
> config.yaml
```yaml
WEBSERVER:
  host: 0.0.0.0
  port: 80
WEBSOCKET:
  host: 0.0.0.0
  port: 8000
```

> namekox run ping
```shell script
2021-01-13 09:45:58,424 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-01-13 09:45:58,425 DEBUG starting services ['ping']
2021-01-13 09:45:58,426 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_websocket.core.entrypoints.app.server.WssServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_pong, ping:namekox_websocket.core.entrypoints.app.handler.WebSocketHandler:wss_pong]
2021-01-13 09:45:58,428 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-01-13 09:45:58,428 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-01-13 09:45:58,429 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_websocket.core.entrypoints.app.server.WssServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:api_pong, ping:namekox_websocket.core.entrypoints.app.handler.WebSocketHandler:wss_pong] started
2021-01-13 09:45:58,429 DEBUG starting service ping dependencies []
2021-01-13 09:45:58,429 DEBUG service ping dependencies [] started
2021-01-13 09:45:58,429 DEBUG services ['ping'] started
2021-01-13 09:46:06,968 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x104e17cd0>, ('127.0.0.1', 54270)), kwargs={}, tid=handle_request)
2021-01-13 09:46:10,019 DEBUG spawn worker thread handle ping:wss_pong(args=(<Request 'http://127.0.0.1:8000/' [GET]>, '7ce2ea32-4d4e-471d-a6a5-89191ace6ea4', u'asdad'), kwargs={}, context={})
2021-01-13 09:46:13,838 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x104e17590>, ('127.0.0.1', 54293)), kwargs={}, tid=handle_request)
2021-01-13 09:46:13,843 DEBUG spawn worker thread handle ping:api_pong(args=(<Request 'http://127.0.0.1/' [GET]>,), kwargs={}, context={})
2021-01-13 09:46:13,844 DEBUG publish {"errs": "", "data": {"api_pong": true}} to channel ping succ
127.0.0.1 - - [13/Jan/2021 09:46:13] "GET / HTTP/1.1" 200 237 0.002497
```
