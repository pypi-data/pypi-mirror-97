#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sys


from logging import getLogger
from eventlet.event import Event
from werkzeug.routing import Rule
from eventlet.websocket import WebSocketWSGI
from namekox_websocket.core.message import WssMessage
from namekox_core.core.friendly import as_wraps_partial
from namekox_core.core.service.entrypoint import Entrypoint
from namekox_websocket.core.messaging import get_message_headers


from .server import WssServer


logger = getLogger(__name__)


class BaseWebSocketHandler(Entrypoint):
    server = WssServer()

    def __init__(self, rule, methods=('GET',), **kwargs):
        self.rule = rule
        self.methods = ('GET',)
        self.accpted = True
        super(BaseWebSocketHandler, self).__init__(**kwargs)

    def setup(self):
        self.server.register_extension(self)

    def stop(self):
        self.accpted = False
        self.server.unregister_extension(self)
        self.server.wait_extension_stop()

    @property
    def url_rule(self):
        return Rule(self.rule, methods=self.methods, endpoint=self)

    def handle_request(self, request):
        def handler(ws_sock):
            sock_id = self.server.hub.add_wsock(ws_sock)
            try:
                self.handle_connect(request, sock_id, ws_sock)
                while self.accpted:
                    data = ws_sock.wait()
                    if data is None:
                        break
                    ws_mesg = self.handle_message(request, sock_id, data)
                    ws_sock.send(ws_mesg.as_json())
            except Exception as e:
                msg = 'ws_sock:{} send msg error {}'.format(sock_id, e.message)
                logger.error(msg)
            finally:
                exc_info = sys.exc_info()
                self.handle_sockclose(request, sock_id, exc_info)
        response = WebSocketWSGI(handler)
        return response

    @staticmethod
    def res_handler(event, context, result, exc_info):
        data = (context, result, exc_info)
        event.send(data)
        return result, exc_info

    def handle_connect(self, request, sock_id, ws_sock):
        pass

    def handle_message(self, request, sock_id, data):
        context, result, exc_info = None, None, None
        try:
            ctxdata = get_message_headers(request)
            args, kwargs = (request, sock_id, data), request.path_values
            event = Event()
            res_handler = as_wraps_partial(self.res_handler, event)
            self.container.spawn_worker_thread(self, args, kwargs,
                                               ctx_data=ctxdata,
                                               res_handler=res_handler)
            context, result, exc_info = event.wait()
        except Exception:
            exc_info = sys.exc_info()
        return context, result, exc_info

    def handle_response(self, request, context, result):
        raise NotImplementedError

    def handle_exception(self, request, context, exc_info):
        raise NotImplementedError

    def handle_sockclose(self, request, sock_id, exc_info):
        self.server.hub.del_wsock(sock_id)


class WebSocketHandler(BaseWebSocketHandler):
    def handle_message(self, request, sock_id, data):
        context, result, exc_info = super(WebSocketHandler, self).handle_message(request, sock_id, data)
        return (
            self.handle_response(request, context, result)
            if exc_info is None else
            self.handle_exception(request, context, exc_info)
        )

    def handle_response(self, request, context, result):
        errs, data = '', result
        return WssMessage(errs=errs, data=data)

    def handle_exception(self, request, context, exc_info):
        exc_type, exc_value, exc_trace = exc_info
        errs, data = exc_value.message, None
        return WssMessage(errs=errs, data=data)
