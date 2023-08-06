#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from .handler import WebSocketHandler


app = type(__name__, (object,), {'wss': WebSocketHandler.decorator})
