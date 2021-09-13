from datetime import datetime
import re
import redis
from common.database import dbconnect





def redis_connect():
    # 使用连接池进行连接
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)  # 实例化连接池
    red = redis.Redis(connection_pool=pool)  # 实例化redis类
    return red


def redis_article_zsort():
    from model.users import Users
    from model.article import Article
    dbsession, md, DBase = dbconnect()
    result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).all()
    # result的数据格式为：[ (<__main__.Article object at 0x113F9150>, '昵称')，() ]
    # 对result进行遍历处理，最终生成一个标准的JSON数据结构

    list = []
    for article, nickname in result:
        dict = {}
        for k, v in article.__dict__.items():
            if not k.startswith('_sa_instance_state'):  # 跳过内置字段
                # 如果某个字段的值是datetime类型，则将其格式为字符串
                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                # 将文章内容的HTML和不可见字符删除，再截取前面80个字符
                elif k == 'content':
                    pattern = re.compile(r'<[^>]+>')
                    temp = pattern.sub('', v)
                    temp = temp.replace('&nbsp;', '')
                    temp = temp.replace('\r', '')
                    temp = temp.replace('\n', '')
                    temp = temp.replace('\t', '')
                    v = temp.strip()[0:80]
                dict[k] = v
        dict['nickname'] = nickname
        list.append(dict)  # 最终构建一个标准的列表+字典的数据结构

    # 将数据缓存到有序集合中
    red = redis_connect()
    for row in list:
        # zadd的命令参数为：（键名，{值:排序依据})
        # 此处将文章表中的每一行数据作为值，文章编号作为排序依据
        red.zadd('article', {str(row): row['articleid']})


# if __name__ == '__main__':
#     redis_article_zsort()