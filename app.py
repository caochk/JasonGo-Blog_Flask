"""
    :author: Jason Cao（曹宸恺）
"""
from flask import Flask, render_template, request, session, abort, make_response, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import os, re, pymysql
from math import ceil

pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder="templates", static_url_path='/', static_folder="static")  # static_url_path用于配置静态资源的基础路径，即从/开始
app.config['SECRET_KEY'] = os.urandom(24)

# 配置数据库连接操作
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/ppnote?charset=utf8'
# 指定SQLAlchemy跟踪数据的更新操作为false
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置连接池大小（默认为5），此处设为100
app.config['SQLALCHEMY_POOL_SIZE'] = 100
# 实例化数据库连接
db = SQLAlchemy(app)



# ////////////////////上下文全局变量////////////////////
@app.context_processor
def gettype():
    type = {
        '1': 'PHP开发',
        '2': 'Java开发',
        '3': 'Python开发',
        '4': 'Web前端',
        '5': '测试开发',
        '6': '数据科学',
        '7': '网络安全',
        '8': 'PP杂谈'
    }
    return dict(article_type=type)


# ////////////////////before_request拦截器////////////////////
# 来实现客户端无论从哪个路由开始访问，都可实现自动登录功能（除了访问一些静态资源&登录、注册页面时无需自动登录）
@app.before_request
def before():
    url = request.path  # 获取客户端请求报文中的URL
    pass_list = ['/user', '/login', '/logout']  # 不进行拦截名单（即无需实现自动登录的白名单）

    # 越过白名单及静态资源
    if url in pass_list or url.endswith('.jpg') or url.endswith('.png') or url.endswith('.js') or url.endswith('.css'):
        pass
    # 只有当 当前处于非登录状态时才有必要去尝试帮用户自动登录
    # 因为没有修改session的有效期，所以现在就是默认值：浏览器关闭后会清空session
    # 也就是说，只要没有关闭浏览器哪怕只是关闭了标签页，再打开博客，也会直接利用session来实现自动登录，此时还不会用到cookie来实现自动登录。
    # 只有浏览器关闭后再打开要再实现自动登录就得依靠cookie了（当然前提是cookie在有效期内）
    # 所以现在可以进一步预想【想要用session实现自动登录】可能只需要1.第一次登录后设置好session['islogin']=True；
    # 2.将session的有效期改长一点。那么在该有效期内就能依靠session实现更加安全的自动登录了
    elif session.get('islogin') is None:
        print('尝试了用cookie实现自动登录2！！！！！！！')
        print(session.get('islogin'))
        # 从用户请求的cookie值中获取信息，然后去尝试自动登录
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username and password:  # 如果cookie中确实存在用于自动登录用的信息，才往下走
            user = Users()
            result = user.find_by_username(username)
            # 拿着用户输入的用户查询数据库查询到了结果且确实只为一条结果，再是密码验证通过，那么就可以登录了
            if len(result) == 1 and result[0].password == password:
                # 在session中保存当前自动登录用户的一系列信息，只要session在有效期内，这些信息可跨路由调用
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role
        print(session.get('islogin'))
    else:
        pass

# 导入蓝本并注册
from controller.index import *
from controller.user import *
from controller.article import *

# 【蓝本一直出现404找不到模板文件错误的原因：注册蓝本需要在app运行前完成】
app.register_blueprint(index)
app.register_blueprint(user)
app.register_blueprint(article)

if __name__ == '__main__':
    app.run(debug=True)
