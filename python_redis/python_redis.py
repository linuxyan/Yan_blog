#!/usr/bin/python
#coding=utf-8

import redis

class AppRedis:

    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0
        self.password = 'foobared'
        self.socket_timeout = 3
        self.r = redis.Redis(host = self.host, port = self.port, db = self.db, password=self.password, socket_timeout=self.socket_timeout)

    def hmset(self,key,datadict):
        return self.r.hmset(key,datadict)

    def hmget(self,*args):
        return self.r.hmget(*args)

    def getkeys(self):
        return self.r.keys()

    def getalldata(self):
        database = []
        allkeys = self.r.keys()
        allkeys.sort(key=lambda x:int(x),reverse=True)
        for id in allkeys:
            item = self.hmget(id,'title','time','tags','md_path')
            item.insert(0,id)
            database.append(item)
        return database

    def getnextid(self):
        allkeys = self.r.keys()
        allkeys.sort(key=lambda x:int(x),reverse=True)
        return int(allkeys[0])+1

    def save(self):
        return self.r.save()

if __name__ == '__main__':
    pass