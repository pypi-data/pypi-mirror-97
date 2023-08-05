# -*- coding: utf-8 -*-
__author__ = 'Henry B. <tubnd.younet@gmail.com>'

from scrapy.exceptions import NotConfigured
import logging

log = logging.getLogger('scrapyx.stormproxies')

class StormProxyMiddleware(object):
    def __init__(self, settings):
        if not settings.getbool('STORMPROXIES_ENABLED', True):
            raise NotConfigured

        self.proxy = settings.get('STORMPROXIES_URL', 'http://127.0.0.1:24000')

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy