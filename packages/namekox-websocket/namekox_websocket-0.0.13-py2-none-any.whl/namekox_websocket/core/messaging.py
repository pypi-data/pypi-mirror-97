#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals

import six
import anyjson


from namekox_websocket.constants import DEFAULT_WEBSOCKET_H_PREFIX


def gen_message_headers(context):
    headers = {}
    for k, v in six.iteritems(context):
        k = '{}-'.format(DEFAULT_WEBSOCKET_H_PREFIX) + k
        headers.update({k: anyjson.serialize(v)})
    return headers


def get_message_headers(message):
    headers = {}
    for k, v in six.iteritems(message.headers):
        p = '{}-'.format(DEFAULT_WEBSOCKET_H_PREFIX)
        k.startswith(p) and headers.update({k[len(p):]: anyjson.deserialize(v)})
    return headers
