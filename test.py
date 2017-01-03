#!usr/bin/env python3
#-*- coding:utf-8 -*-
def more(c):
    key = "金鹰电竞"
    urls=[]
    count=[]
    for i in range(c):
        urldemo = "http://news.baidu.com/ns?word="+key+"&pn="+str(20*i)+"&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0"
        urls.append(urldemo) 
    return (urls)
print(more(10))

