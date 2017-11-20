__author__ = "Guilherme Matsumoto"

####
# This module requires de scrape-linkedin package, version 0.1. This is not an official package and has no support.
#
#
####

from pylinkedin.utils import CustomRequest
from pylinkedin.scraper import LinkedinItem

class LinkedinParser(object):
    def __init__(self, initial_url="https://www.linkedin.com/in/karl-dessenne-033390140/", max_pages=100, proxy_list=None):
        self.url_list = []
        self.url_count = 0
        if proxy_list is not None:
            self.proxy_list = proxy_list
        else:
            self.proxy_list = [{'http': 'http://155.94.205.196:3128'}, {'http': 'http://203.74.4.4:80'},
                               {'http': 'http://139.162.27.112:3128'}, {'http': 'http://46.105.51.183:80'},
                               {'http': 'http://139.162.27.112:3128'}, {'http': 'http://46.105.51.183:80'},
                               {'http': 'http://110.78.168.152:55555'}, {'http': 'http://54.36.182.96:3128'},
                               {'http': 'http://61.28.162.229:3128'}, {'http': 'http://118.189.172.136:80'},
                               {'http': 'http://111.68.45.227:8080'}, {'http': 'http://167.114.47.231:3128'}]
        self.c = CustomRequest(list_proxies=self.proxy_list)