import redis
from instagram import  app,db
from instagram.models import Image

# redis服务器的IP地址和端口号
redis_host = app.config['REDIS_HOST']
redis_port = app.config['REDIS_PORT']


# 关注功能
def follow(followID, UserID):
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    r.sadd(str(followID) + "follower", UserID)
    r.sadd(str(UserID) + "following", followID)

# 取消关注
def unfollow(followID, UserID):
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    r.srem(str(followID) + "follower", UserID)
    r.srem(str(UserID) + "following", followID)
    

# 是否关注
def isfollow(followID, UserID):
    if followID == UserID:
        return True
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    return r.sismember(str(UserID) + "following", followID)


# 获取关注列表
def getfollowing(UserID):
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    return r.smembers(str(UserID) + "following")

# 获取粉丝列表

def getfollowed(UserID):
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    return r.smembers(str(UserID) + "follower")

