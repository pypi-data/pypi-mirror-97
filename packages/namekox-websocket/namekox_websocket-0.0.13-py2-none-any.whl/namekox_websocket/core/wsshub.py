#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import sys


from logging import getLogger
from namekox_core.core.spawning import SpawningProxy
from namekox_websocket.core.message import WssMessage
from namekox_core.core.generator import generator_uuid
from namekox_core.core.friendly import as_singleton_cls, ignore_exception


reload(sys)
sys.setdefaultencoding('utf-8')


logger = getLogger(__name__)


@as_singleton_cls
class WebSocketHub(object):
    def __init__(self):
        self.sockets = {}
        self.wsocket_2_channel = {}
        self.channel_2_wsocket = {}

    def add_wsock(self, socket):
        sock_id = generator_uuid()
        self.sockets[sock_id] = socket
        return sock_id

    def del_wsock(self, sockid):
        channel = self.wsocket_2_channel.pop(sockid, set())
        for sockid_channel in channel:
            self.unsubscribe(sockid_channel, sockid)
        ws_sock = self.sockets.pop(sockid, None)
        ws_sock and ignore_exception(ws_sock.close)()

    def broadcast(self, channel, message):
        succ_msg = None
        if not isinstance(message, WssMessage):
            fail_msg = 'message {} no isinstance of {}, ignore'.format(message, WssMessage)
            logger.warn(fail_msg)
        else:
            message = message.as_json()
            sockids = self.channel_2_wsocket.get(channel, set())
            sockets = [self.sockets.get(id) for id in sockids if id in self.sockets]
            SpawningProxy(sockets).send(message)
            succ_msg = 'publish {} to channel {} succ'.format(message, channel)
        succ_msg and logger.debug(succ_msg)

    def subscribe(self, channel, sock_id):
        self.wsocket_2_channel.setdefault(sock_id, set())
        self.wsocket_2_channel[sock_id].add(channel)
        self.channel_2_wsocket.setdefault(channel, set())
        self.channel_2_wsocket[channel].add(sock_id)

    def unsubscribe(self, channel, sock_id):
        self.wsocket_2_channel.get(sock_id, set()).discard(channel)
        self.channel_2_wsocket.get(channel, set()).discard(sock_id)
