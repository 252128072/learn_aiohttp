#-*- coding:utf-8 -*-
#!usr/bin/env python3 
import asyncio
from reptile import find
from aiohttp import web,MultiDict
import aioredis
import json


async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def data(request):
    await asyncio.sleep(0.5)
    #start = request.match_info['starttime']
    #end = request.match_info['endtime']
    #print(start,end)
    start = request.GET['starttime']
    end = request.GET['endtime']

    #client = redis.StrictRedis('127.0.0.1',6379)
    #hashVal = client.hget('index',start)
    #post_params = MultiDict()
    #multidict = await find('20161001','20161212')
    news_list = await find(start, end)

    #for i in news_list:
    #    print(i)
    #text = '<h1>%s</h1>' % await find(start=20161010,end=20161212)
    #return web.Response(body=b'<h1></h1>')

    #return web.Response(body=text.encode('utf-8'))
    return web.Response(body=json.dumps(news_list).encode())


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/HOST/api/crawler/gec/news', data)
    #app.router.add_route('GET', '/starttime={starttime}&endtime={endtime}', data)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
