from instagram import  app,db
from instagram.models import Image
import happybase


conn = happybase.Connection("127.0.0.1", 9090)
table = conn.table("follow")



# 关注功能
def follow(followID, UserID):
    table.put(str(UserID),{"following:"+str(followID):str(followID)})
    table.put(str(followID),{"followers:"+str(UserID):str(UserID)})

# 取消关注
def unfollow(followID, UserID):
    table.delete(str(UserID),{"following:"+str(followID):str(followID)})
    table.delete(str(followID),{"followers:"+str(UserID):str(UserID)})
    

# 是否关注
def isfollow(followID, UserID):
    if followID == UserID:
        return True
    follow = table.cells(str(UserID),"following:"+str(followID))
    return len(follow) != 0 

# 获取关注列表
def getfollowing(UserID):
    result = table.scan(str(UserID),str(UserID),filter="FamilyFilter(=,'binary:following')")
    ids = []
    for key,value in result:
        print(key)
        print(value)
        ids += value.values()
    return ids

# 获取粉丝列表

def getfollowed(UserID):
    result = table.scan(str(UserID),str(UserID),filter="FamilyFilter(=,'binary:followers')")
    ids = []
    for key,value in result:
        ids += value.values()
    return ids


