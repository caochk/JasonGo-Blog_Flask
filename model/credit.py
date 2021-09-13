from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()

# credit表的关系模型
class Credit(DBase):
    __table__ = Table('credit', md, autoload=True)

    # 插入积分明细数据
    def insert_detail(self, type, target, credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'), category=type, target=target,
                        credit=credit, createtime=now, updatetime=now)  # 实例化credit模型类
        dbsession.add(credit)  # 将新创建的记录添加到数据库会话
        dbsession.commit()  # 提交数据库会话