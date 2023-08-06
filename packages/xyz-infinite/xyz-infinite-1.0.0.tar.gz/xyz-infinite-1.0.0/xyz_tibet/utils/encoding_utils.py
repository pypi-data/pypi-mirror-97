# -*- coding:utf-8 -*-

import hashlib
from datetime import datetime


def ensure_utf8(str1):
    if str1 is None:
        return ''
    if isinstance(str1, unicode):
        return str1.encode('utf-8')
    return str1


def ensure_unicode(str1):
    if str1 is None:
        return u''
    if isinstance(str1, unicode):
        return str1
    elif isinstance(str1, (int, float)):
        return str1
    elif isinstance(str1, datetime):
        return str1.strftime("%Y")
    else:
        return str1.decode('utf-8')


def md5_hex(url):
    """
    返回url的utf8编码对应的hex digest
    """
    url = ensure_utf8(url)
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def encode_for_client(content):
    """
    为了fix客户端的bug：\n, %, "
    """
    ENCODE_DICT = {'\n': ' ', '%': u'％', '"': "'", '/': u'/'}

    for key, value in ENCODE_DICT.items():
        content = content.replace(key, value)

    return content


def convert_to_unicode_string(value):
    """
    将value转换成unicode格式的字符串
    """
    return ensure_unicode(str(ensure_utf8(value)))
