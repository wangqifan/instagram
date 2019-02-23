from instagram import app,db
from flask_script import Manager

manager=Manager(app)

@manager.command
def init_datebase():
    db.drop_all()         # 删除所有的表
    db.create_all()       # 重建表


if __name__ == "__main__":
    init_datebase()