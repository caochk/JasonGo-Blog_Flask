from sqlalchemy import Table
from common.database import dbconnect
import time, random
from flask import session

dbsession, md, DBase = dbconnect()

# users表的关系模型
class Users(DBase):
    __table__ = Table('users', md, autoload=True)

    # 查询用户名（用于注册时判断用户名是否已注册、还用于登录校验）
    def find_by_username(self, username):
        result = dbsession.query(Users).filter_by(username=username).all()
        return result

    # 用户注册（将数据写入数据库users表）
    def do_register(self, username, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')  # 用户进行注册时的时间
        nickname = username.split('@')[0]  # 此处默认将邮箱前缀作为用户名
        avatar = str(random.randint(1, 15)) + '.png'  # 从15张默认头像图片中随机选取一张作为用户初始头像（初步设想如此）
        user = Users(username=username, password=password, role='user', nickname=nickname, credit=50,
                     avatar=avatar, createtime=now, updatetime=now)  # 实例化users模型类
        dbsession.add(user)  # 将新创建的记录添加到数据库会话
        dbsession.commit()  # 提交数据库会话
        return user

    # 增减用户积分（阅读收费文章会扣除相应积分）
    def update_credit(self, credit):
        user = dbsession.query(Users).filter_by(userid=session.get('userid')).one()
        user.credit += credit
        dbsession.commit()