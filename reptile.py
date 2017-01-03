#!usr/bin/env python3
# -*-coding:utf-8 -*-
import re
import urllib.request
import aioredis
import uuid
from datetime import datetime, timedelta
import asyncio
import tqdm

async def getHtml(url):
    page = urllib.request.urlopen(url).read()
    html = page.decode('utf-8')
    return html

async def time_tool(list_i):
    return (list_i[0:11].replace("年","").replace("月","").replace("日",""))

async def downloading(root):
    regurl= re.compile(r'class="c-title"><a href="(.+?)"')
    regtitle = re.compile(r'target=\"_blank\"(?:\s|\n)*?>(.+?)</a></h3>')
    reg_author = re.compile(r'<p class="c-author">(.+?)&nbsp;&nbsp;')
    reg_time = re.compile(r'&nbsp;&nbsp;(.+?)</p>')
    list_url = re.findall(regurl, root)
    list_author = re.findall(reg_author, root)
    list_time = re.findall(reg_time, root)
    list_title = re.findall(regtitle,root)
    #client = redis.StrictRedis('127.0.0.1',6379,encoding='utf-8') 
    client = await aioredis.create_redis(('localhost', 6379))
    for i, j, k, l in zip(list_time,list_title,list_url,list_author):
       #hmDict={'time':i,'title':j.replace("<em>","").replace("</em>",""),'url':k,'source':l}

       boot_time = await time_tool(i)
       #print(time_tool(i))
       id = str(uuid.uuid1())
# time的集合
       await client.sadd(boot_time,id)
       await client.hmset(id,'time',i,'title',j.replace("<em>","").replace("</em>",""),'url',k,'source',l)
#1.存时间戳对应具体时间段(通一天的放到一个set中) 2.存time,title,url,source
       #val_set = client.smembers('20161010')
       #val_hash = client.hgetall(client.spop('20161010'))
       #print ("get time set value",val_set) 
       #print ("get hash-value",val_hash) 
    #时间戳
    #while 1:
       # await asyncio.sleep(0.5)
       # a = '20161001'
    #client.flushdb()


async def find(start_time,end_time):
    if not len(start_time) == 8 or not len(end_time) == 8:
        print('数据格式错误1')
        return False
    try:
        start_time = datetime.strptime(start_time, '%Y%m%d')
        end_time = datetime.strptime(end_time, '%Y%m%d')
        if end_time <= start_time:
            print('结束时间大于开始时间')
            return False
        count_time = start_time
        #print(repr(count_time))
        dict1 =[]
        enum = 0
        client = await aioredis.create_redis(('localhost', 6379))
        while count_time <= end_time:
            allday = await client.scard(str(count_time)[0:10].replace("-",""))
            for i in range(allday):
            #对应个数的id数
                c = await client.spop(str(count_time)[0:10].replace("-",""))
                #c = await client.srandmember(str(count_time)[0:10].replace("-",""))
            #print(type(c),'\n')
                #print(count_time)
            #print(c.decode(),'\n')
                t1 = await client.hget(c.decode(), "time")
                t2 = await client.hget(c.decode(), "title")
                t3 = await client.hget(c.decode(), "url")
                t4 = await client.hget(c.decode(), "source")
                enum = enum + 1
                dict1.append(('time:', t1.decode('utf-8'), 'title:', t2.decode('utf-8'), 'url:', t3.decode('utf-8'),'source:', t4.decode('utf-8')))
                #return dict
                #return (enum, ':', 'time:', t1.decode('utf-8'), 'title:', t2.decode('utf-8'), 'url:', t3.decode('utf-8'),'source:', t4.decode('utf-8'))
            count_time += timedelta(days=1)
        #print(dict1)
        return dict1
    except ValueError:
        print('数据格式错误2')
        return []


async def clean():
    client = await aioredis.create_redis(('localhost', 6379))
    await client.flushdb()
    return

async def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        await f


async def more_root(key,count):
    #按照关键词从百度新闻中，生成前count页的url
    #key = "金鹰电竞"
    urls = []
    for i in range(count):
        urldemo = "http://news.baidu.com/ns?word=" + key + "&pn=" + str(20*i) + "&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0"
        urls.append(urldemo)
    #print(urls)
    return(urls)


async def main():
    #root = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=%E9%87%91%E9%B9%B0%E7%94%B5%E7%AB%9E'
    #html = getHtml(root)
    #clean()
    urls = await more_root("%E9%87%91%E9%B9%B0%E7%94%B5%E7%AB%9E",10)
    for root in urls:
        html = await getHtml(root)
        await downloading(html)

    #downloading（html）依次抓取url中的内容
    #redis 清空在redsi-cli中使用flushall
    #await find('20161001', '20161212')
    #print(await find('20161001','20161212'))

    #目前调试到，执行一次抓一次，pop一次。

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()



