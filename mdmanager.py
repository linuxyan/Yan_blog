#!/usr/bin/python
#coding=utf-8

import os,sys,time,getopt
from python_redis import python_redis
basedir = os.path.abspath(os.path.dirname(__file__))

def main(title,tags,md_path,rid=None):
    appredis = python_redis.AppRedis()
    if rid:
        rid=int(rid)
    else:
        rid = appredis.getnextid()
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    data = {'title':title,'time':date,'tags':tags,'md_path':md_path}
    appredis.hmset(rid,data)

def Usge():
    print 'mdmanager.py usage:'
    print '-h,--help:打印帮助信息.'
    print '-i,--id:指定文章ID号(可选).'
    print '-t,--title:指定文章标题.如:--title="测试标题"'
    print '-g,--tags:指定文章标签.以空格分割.如:--tags="python markdown"'
    print '-f,--file:指定文章MD文件路径,路径需要加默认前缀: "markdown/".如:--file="markdown/helloword.md"'
    print '如果指定id号,如果此ID有内容,则为更新此ID的内容,如果此ID没有内容,则为指定ID新加内容!'

if __name__ == '__main__':
    rid = None
    try:
        opts,agrs = getopt.getopt(sys.argv[1:],"hi:t:g:f:",["help","title=","tags=","file="])
    except getopt.GetoptError,err:
        print str(err)
        Usge()
        sys.exit(2)
    if opts:
        for key,value in opts:
            if key in ('-h','--help'):
                Usge()
                sys.exit(1)
            elif key in ('-i','--id'):
                rid = value
            elif key in ('-t','--title'):
                title = value
            elif key in ('-g','--tags'):
                tags = value
            elif key in ('-f','--file'):
                md_path = value
            else:
                assert False,"Unknown option!"

        if title and tags and os.path.exists(basedir+'/'+md_path):
            if rid:
                main(title=title,tags=tags,md_path=md_path,rid=rid)
            else:
                main(title=title,tags=tags,md_path=md_path)
            print "Add content success!"
        else:
            print "title:%s"%title
            print "tags:%s" %tags
            print "file:%s" %md_path
            print "Error: Key error!"
            sys.exit(3)
    else:
        Usge()
        sys.exit(1)
