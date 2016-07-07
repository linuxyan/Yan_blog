#Centos6使用 virtualenv环境部署Flask项目

-------------------
>前言：由于之前是在mac上开发了一个项目，用到的python版本是2.7.10 。部署到生产环境的时候，Centos6系列自带的python版本只有python2.6.结果项目跑不起来，于是使用virtualenv来创建一个python2.7.10的虚拟环境。

**virtualenv**通过创建独立Python虚拟运行环境, 来解决依赖、版本以及间接权限问题. 多个Python环境相互独立，互不影响, 使用virtualenv可以解决这些问题：
- **权限不足** ：通过创建独立虚拟环境，在没有系统权限的情况下在虚拟环境里面安装新模块。
- **版本隔离** ：不同的应用可以创建不同的虚拟环境来实现调用不同的模块版本。
- **独立升级** ：可以升级指定的环境的指定模块，不影响其他应用的使用。


##virtualenv安装
####使用pip安装
```python
pip install virtualenv
```
####使用easy_install安装
```python
easy_install virtualenv
```

##virtualenv基本使用
>使用<code>virtualenv</code>创建指定版本的python虚拟环境的前提是本机上要安装了<code>该版本的python</code>。这里我要使用python2.7.10版本的python，<code>必须</code>要先在机器上安装python2.7.10.

在centos6安装python2.7.10
```shell
yum install zlib-devel openssl-devel
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar zxvf Python-2.7.10.tgz 
./configure --prefix=/usr/local/python27
make 
make install
```
><code>zlib-devel  openssl-devel</code>这两个包一定要<code>安装之后</code>再编译python，要不创建虚拟环境的时候，会报：
><code>ImportError: No module named  zlib</code>
><code>ImportError: No module named <code>

####创建python虚拟环境ENV
```python
virtualenv ENV
```
>创建一个虚拟环境ENV，会产生一个`ENV`目录，该目录就是一个虚拟的python环境。
>创建的虚拟环境默认会安装`pip`和`easy_install`
>**`lib`** 所有安装的python库都会放在这个目录中的lib/pythonx.x/site-packages/下
>**`bin`** 是在当前环境是使用的python解释器

####附加参数
```python
virtualenv --system-site-packages ENV
virtualenv --no-site-packages ENV
```
>参数`--system-site-packages`会继承/usr/lib/python2.7/site-packages下的所有库.
>参数`--no-site-packages`不会把已经安装到系统Python环境中的所有第三方包复制过来,这样我们就创建了一个不带任何第三方包的`干净`的Python运行环境。
>最新版本virtualenv会把访问全局site-packages作为`默认`行为.

####创建指定python版本的虚拟环境
```python
virtualenv -p /usr/local/python27/bin/python2.7  ENV
```
>-p参数或者--python=参数可以创建一个指定python版本的虚拟环境.

####激活virtualenv
```python
source ./ENV/bin/activate #激活之后，终端前面会加上当前虚拟环境的名称，如果ENV
(ENV)
```

####关闭virtualenv
```python
deactivate   #退出当前虚拟环境
```

##部署Flask项目
####在`ENV`虚拟环境中安装项目的依赖包
```
source ./ENV/bin/activate 
pip install -r requirements.txt
deactivate   
```
####安装uwsgi
```
source ./ENV/bin/activate 
pip install uwsgi
deactivate 
```
####创建uwsgi的配置文件Yan.ini
```ini
[uwsgi]
master = true
vhost = true
workers = 5
reload-mercy = 10
vacuum = true
max-requests = 1000
limit-as = 256
chmod-socket = 666
socket = /tmp/uwsgi_Yan_blog.sock
venv = /var/www/ENV/
chdir = /var/www/Yan_blog
module = Yan_blog
callable = app
daemonize = /var/log/Yan_blog.log
```
>**`master`**  启动主进程.
>**`vhost`** 开启虚拟主机模式.
>**`workers`** 开启几个工作进程.
>**`reload-mercy`** 平滑重启等待最大时间.超出此时间还没处理完的请求会被强行结束.
>**`vacuum`** 当服务器退出的时候自动删除unix socket文件和pid文件.
>**`max-requests`** 为每个工作进程设置请求数的上限,上述配置设置工作进程每处理1000个请求就会被回收重用。
>**`limit-as`** 限制每个uWSGI进程的虚拟内存使用数。如果超出,则会使程序报内存错误.
>**`chmod-socket`** 设置socket文件的权限.
>**`socket`** 指定uwsgi的客户端将要连接的socket的路径,也可以设置为端口.
>**` venv`**   为python程序设置指定的虚拟环境，就是我们刚才创建的ENV.
>**`chdir `** 在失去权限前，使用chdir()到指定目录(就是项目的目录)。
>**`module`** 加载指定的python WSGI模块(项目的启动文件).
>**`callable`** 设置在收到请求时，哪个变量将被调用，(`app = Flask(__name__`) 就是这里的app。
>**`daemonize`**  使进程在后台运行，并将日志打到指定的日志文件或者udp服务器.

####用uwsgi启动flask项目
```python
/var/www/ENV/bin/uwsgi /var/www/Yan_blog/Yan.ini
```
>可以查看日志文件/var/log/Yan_blog.log来查看是否启动成功。

####使用nginx代理转发到uwsgi
在nginx配置文件中新建一个server段，配置转发到uwsgi
```nginx
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/uwsgi_Yan_blog.sock;
    }
```

启动nginx就可以通过nginx去访问flask的项目啦。
