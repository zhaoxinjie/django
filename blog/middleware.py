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

import logging

logger = logging.getLogger('blog.middleware')


class AccessMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_exception(self, request, exception):
        return HttpResponse(exception)

    def process_request(self, request):
        meta = request.META
        if 'HTTP_REMOTE_ADDR' in meta:
            logger.info("[%s] PATH_INFO=%s, REMOTE_ADDR=%s, HTTP_USER_AGENT=%s, "
                        "REQUEST_METHOD=%s, QUERY_STRING=%s" % (
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            meta['PATH_INFO'], meta['HTTP_REMOTE_ADDR'], meta['HTTP_USER_AGENT'],
                            meta['REQUEST_METHOD'], meta['QUERY_STRING']))
        # logger.info('meta: ' + str(meta))
        # 使用nginx代理添加了remote_addr
        # if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
        #     client_ip = request.META['HTTP_X_FORWARDED_FOR']
        #     client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
        # else:
        #     client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip

        if 'HTTP_REMOTE_ADDR' in request.META:
            client_ip = request.META['HTTP_REMOTE_ADDR']
        else:
            client_ip = request.META['REMOTE_ADDR']

        if client_ip:
            uobj = Userip()
            uobj.ip = client_ip
            uobj.save()
        return None

    def process_response(self, request, response):
        return response
