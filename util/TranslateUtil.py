#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2019/6/5
Desc  : youdao translate util

https://ai.youdao.com/docs/doc-trans-api.s#p04
https://ai.youdao.com/docs/doc-trans-api.s#p10
"""

import hashlib
import sys
import uuid

import HttpUtil
import Jsonutil
from DateUtil import DateUtil

reload(sys)
sys.setdefaultencoding('utf8')

YOUDAO_URL = "http://openapi.youdao.com/api"
YOUDAO_API_KEY = "1cfc98fa253d2112"
YOUDAO_APP_SECRET = "YCBsopB8IIW3yqyUpqauykT0R2nwmNGK"


class Translate:
    def __init__(self):
        pass

    # sign
    def encrypt(self, sign):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    # translate text.  return list type
    def translate(self, text):
        text = unicode(text)
        salt = str(uuid.uuid1())
        curtime = str(DateUtil().getCurrentTimeStamp())
        signStr = YOUDAO_API_KEY + self.truncate(text) + salt + curtime + YOUDAO_APP_SECRET
        params = {'q': text, 'from': 'auto', 'to': 'auto', 'appKey': YOUDAO_API_KEY, 'salt': salt,
                  'sign': self.encrypt(signStr), 'signType': 'v3', 'curtime': curtime}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = HttpUtil.http_get(YOUDAO_URL, params=params, header=headers)
        if not response:
            return u'未能翻译'
        # print Jsonutil.parse_date(response)
        # print Jsonutil.loads(response)['query']
        # print Jsonutil.loads(response)['translation']
        return Jsonutil.loads(response)['translation']


if __name__ == '__main__':
    tran = Translate()
    print tran.translate('你好 我好')
