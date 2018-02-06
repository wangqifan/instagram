from instagram import app,db
from flask_script import Manager

manager=Manager(app)

@manager.command
def init_datebase():
    db.drop_all()
    db.create_all()


print('23')
init_datebase()