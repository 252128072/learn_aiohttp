#usr/bin/env python3 
# -*-coding:utf-8 -*-

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import async_timeout
from collections import namedtuple

Node = namedtuple("Node", ["url", "re", "callback"])


class AvGot(object):  
  _ENTRY = "ENTRY_NODE"
  def __init__(self, loop=None):
    self._prev_node = None

    self.headers = {
      "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1)"
      " AppleWebKit/537.36 (KHTML, like Gecko)"
      " Chrome/54.0.2840.87 Safari/537.36"),
    }
    self.conn = aiohttp.TCPConnector(verify_ssl=False)
    self.session = aiohttp.ClientSession(loop=loop,
                    connector=self.conn,
                    headers=self.headers)

    self.pipe = {}
    self.queue = asyncio.Queue()

  async def fetch(self, url=""):
    with async_timeout(10):
      async with self.session.get(url) as resp:
        return await resp.text()

  async def extract(self, url="", regexp=r''):
    html = await self.fetch(url)
    matches = re.findall(regexp, html)
    return matches

  def entry(self, url='', regexp=r''):
    def wrapper(callback):
      node = Node(url, regexp, callback)
      if self.pipe.get(self._ENTRY) is None:
          self.pipe[self._ENTRY] = node
      else:
          self.pipe[self.prev_node.callback] = node
      self._prev_node = node
    return wrapper

  def register(self, regexp=r''):
    return self.entry("",regexp)
   

  def close(self):
    self.session()
    self.loop.close()
  def run(self):
    pass

loop = asyncio.get_event_loop()
av = AvGot(loop)


ROOT = 'http://news.baidu.com/ns?word=金鹰电竞&pn=20&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0'
retime = re.compile()
retitle = re.compile()
relink = re.compile()
resource = re.compile()

@av.entry(ROOT,retime):
async def entry_gettime(result):
     #db.save(result)
    def clean(row):
        return ("https://movie.douban.com{}".format(row[0]), row[1])
    return list(map(clean, result))[:2]

av.run()
av.close()


@asyncio.coroutine

@asyncio.coroutine


