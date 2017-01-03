#-*- coding:utf-8 -*-
#!usr/bin/env python3

import redis

client = redis.StrictRedis('127.0.0.1',6379)
dict1 = {'time':'2013','title':'中问','url':'www.www'}
#client.hset('time','title',['list1','list2','list3'])
#hashVal = client.hget('time','title')
client.hmset('hash_test1',dict1)
#print("get hash value1:",client.hgetall('hash_test1'))

client.sadd('20161001','201610016:00')
client.sadd('20161001','201610015:00')
print(client.smembers('20161001'))

client.flushdb()
