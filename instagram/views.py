from instagram import  app,db
from instagram.models import Image,User,Comment
from flask import render_template, redirect, request, flash, get_flashed_messages, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
import random, hashlib, json, uuid, os
from instagram.qiniusdk import qiniu_upload_file

# 首页

@app.route('/')
@login_required          # 需要登陆才能访问
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html',images=images)

# 图片详情页

@app.route('/image/<int:image_id>/')
@login_required
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
    return render_template('pageDetail.html', image=image, comments=comments)

# 用户注册模块

@app.route('/reg/',methods={'post','get'})
def reg():
    username=request.values.get('username').strip()     # 获取用户名
    password=request.values.get('password').strip()     # 获取密码
    if username=='' or password=='':                    # 判断用户名和密码是不是为空字符串
        return render_template('login.html',msg=u'用户名或密码不能为空')
    user = User.query.filter_by(username=username).first()  #查询数据库判断用户名是不是已经存在
    if user != None:
        return render_template('login.html',msg=u'用户名已经存在')   # 用户名已经存在 注册失败
    salt = '.'.join(random.sample('01234567890abcdefghigABCDEFGHI', 10)) # 生成一个随机字符串 
    m = hashlib.md5()
    m.update((password + salt).encode("utf-8"))         # 调用md5 哈希函数 生成密文
    password = m.hexdigest()
    user = User(username, password, salt)                # 创建用户对象
    db.session.add(user)                                 
    db.session.commit()                                  # 向数据库中插入用户
    login_user(user)
    next = request.values.get('next')                    # 跳转到原来页面
    if next != None and next.startswith('/'):
        return redirect(next)
    return redirect('/loadhead/')                        # 跳转到加载头像页面

# 访问登陆页面，注册也是这个页面

@app.route('/login/',methods={'get','post'})
def login():
    return render_template('login.html')         # 渲染登陆摸板页面

# 登陆

@app.route('/relogin/',methods={'get','post'})
def relogin():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return render_template('login.html', msg=u'用户名或密码不能为空')

    user = User.query.filter_by(username=username).first()
    if user == None:
        return render_template('login.html', msg=u'用户名不存在')

    m = hashlib.md5()
    m.update((password + user.salt).encode('utf-8'))
    if (m.hexdigest() != user.password):
        return render_template('login.html', msg=u'密码错误')
    login_user(user)
    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)

    return redirect('/')

# 登出页面

@app.route('/logout/',methods={'get','post'})
def logout():
    logout_user()
    return redirect('/')

# 加载头像

@app.route('/loadhead/',methods={'GET','POST'})
def loadhead():
    if request.method == "POST":     # 请求方式是POST 
        file = request.files['file']               # 获取文件 也就是头像
        file_ext = ''
        if file.filename.find('.') > 0:
            file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
            print(file_ext)
        if file_ext in app.config['ALLOWED_EXT']:     # 判断文件格式是不是符合我们的要求 app.config['ALLOWED_EXT'] 配置了我们允许的格式        
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
            url = qiniu_upload_file(file, file_name,len(file.read()))   # 调用七牛SDK 上传图片 七牛会返回图片的URL
            if url != None:
                user=User.query.get(current_user.id)
                if user!=None:
                    user.head_url=url
                    db.session.commit()

        return redirect('/')
    else:  # 请求是get方式 前往头像上传页面
        return render_template('loadheadimage.html')

# 访问个人主页 url中<int:user_id> user_id 是用户的ID

@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).order_by(db.desc(Image.id)).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)

# 上传一条动态

@app.route('/upload/', methods={"post"})
@login_required
def upload():
    file = request.files['file']
    # http://werkzeug.pocoo.org/docs/0.10/datastructures/
    # 需要对文件进行裁剪等操作
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        url = qiniu_upload_file(file, file_name,len(file.read()))
        #url = save_to_local(file, file_name)
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)

#  /profile/images/<int:user_id>/<int:page>/<int:per_page>/
# <int:user_id> 用户的ID
# <int:page> 第几页
# int:per_page> 一页有几张

@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)


# 添加评论

@app.route('/addcomment/', methods={'post'})
@login_required
def add_comment():
    image_id = int(request.values['image_id'])     # 获取图片ID
    content = request.values['content']            # 获取评论内容
    comment = Comment(content, image_id, current_user.id)  # 生产评论对象
    db.session.add(comment)
    db.session.commit()                                    # 插入数据库
    return json.dumps({"code":0, "id":comment.id,
                       "content":comment.content,
                       "username":comment.user.username,
                       "user_id":comment.user_id})
