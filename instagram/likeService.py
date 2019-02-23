import redis
from instagram import  app,db
from instagram.models import Image

# redis服务器的IP地址和端口号
redis_host = app.config['REDIS_HOST']
redis_port = app.config['REDIS_PORT']


# 点赞功能
# 从dislike集合删除掉用户ID 
# 从like集合增加用户ID

def like(imgeID, UserID):
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    r.srem(str(imgeID) + "dislike", UserID)
    r.sadd(str(imgeID) + "like", UserID)
    likecount = r.scard(str(imgeID) + "like")
    dislikecount = r.scard(str(imgeID) + "dislike")
    image = Image.query.filter_by(id = imgeID).first()
    image.likecount = likecount
    # image.dislikecount =dislikecount
    db.session.commit() 
    return likecount

def dislike(imgeID, UserID):
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    r.srem(str(imgeID) + "like", UserID)
    r.sadd(str(imgeID) + "dislike", UserID)
    likecount = r.scard(str(imgeID) + "like")
    dislikecount = r.scard(str(imgeID) + "dislike")
    image = Image.query.filter_by(id = imgeID).first()
    image.likecount = likecount
    # image.dislikecount =dislikecount
    db.session.commit() 
    return likecount


