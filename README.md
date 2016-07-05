# Yan_blog
基于markdown写作的博客.



##更新文章
>没有图形化界面更新，使用markdown写好文章之后，放倒markdown目录，通过mdmanager.py文件插入redis.

Yan-Pro:Yan_blog yan$ python mdmanager.py 
mdmanager.py usage:
-h,--help:打印帮助信息.
-i,--id:指定文章ID号(可选).
-t,--title:指定文章标题.如:--title="测试标题"
-g,--tags:指定文章标签.以空格分割.如:--tags="python markdown"
-f,--file:指定文章MD文件路径,路径需要加默认前缀: "markdown/".如:--file="markdown/helloword.md"
如果指定id号,如果此ID有内容,则为更新此ID的内容,如果此ID没有内容,则为指定ID新加内容!
