# instagram
使用flask仿instagram



## 项目介绍
   使用flask构建的图片社交网站,是牛客网的初级项目，增加了点赞，关注，TimeLine等功能
   
   
   
## 所用技术

 * 数据库
    * sqlite
    * 七牛云
 * 数据库访问
   * flask-sqlalchemy
   * 七牛sdk
 * web框架
   * flask
 * 测试
   * unittest 
   
## 安装依赖

~~~
        pip install -r requirements.txt
~~~
   
## 重建数据库

~~~
        python manage.py
~~~

## 运行web App 

~~~
        python serverrun.py
~~~
## TimeLine的实现
    
类似于微信朋友圈，还有发的动态按时间排序，是feed流中的一种。主要有push和pull两种方式
* push 写放到，写放大，每发一条动态将会写入关注者的feed流中，适合于微信这种好友有限的场景，实现简单。但是如果像微博这种有大V具有千万粉丝，那。。。
* pull 读放大，用户会将自己和自己关注的用户的动态读取到。比较复杂，是主流方式。
在master分支中，关注信息放在了redis中，hbase分支将关注信息放在了hbase中

 
 
