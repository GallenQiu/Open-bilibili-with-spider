import pymongo
from pymongo.collection import Collection

#建立连接
client=pymongo.MongoClient('localhost',27017)
#建立数据库
db=client["bilibili"]

#从原有的txt文件导入share_id：
def insert(dict_data,code):
    #表的对象化
    mgtable=Collection(db,'mbilibili_{}'.format(code))

    mgtable.insert(dict_data)