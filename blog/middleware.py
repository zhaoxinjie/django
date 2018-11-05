#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: zhao
@contact: zhaoxinjie2016@gmail.com
@software: PyCharm
@file: middleware.py
@time: 2018/11/5 23:34
"""

import time
from django.http import HttpResponse

from blog.models import Userip


class AccessMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return HttpResponse(exception)

    def process_request(self, request):
        meta = request.META
        print("[%s] PATH_INFO=%s, REMOTE_ADDR=%s, HTTP_USER_AGENT=%s" % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            meta['PATH_INFO'], meta['REMOTE_ADDR'], meta['HTTP_USER_AGENT']))

        if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
            client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
        else:
            client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
        print(client_ip)

        uobj = Userip()
        uobj.ip = client_ip
        uobj.save()
        return None

    def process_response(self, request, response):
        return response
