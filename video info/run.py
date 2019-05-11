import requests,json,time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from DBUtils.PooledDB import PooledDB
from mbi_mysql import db
import mysql.connector
from mbi_Mongo import insert

class Mbilibili:
    def __init__(self,tid,dbname):
        self.page_list=Queue()
        self.data_list=[]
        self.tid=tid#视频分类编号（通过runj查询分区编号.py可查询）
        self.count=0
        self.max=0
        self.dbname=dbname

    def insert_to_mysql(self):
        '''初始化mysql连接池'''
        print('储存数据库中。。。')
        dbpool = PooledDB(mysql.connector,10,host='localhost',user='root',passwd='199756',db='bilibili',port=3306) #4为连接池里的最少连接数
        while True:
            if len(self.data_list)==0:
                break
            conn = dbpool.connection()  # 每次入库只需要建立connection()就可以，而不用再次初始化。
            c = db(conn, self.data_list.pop())
            c.insert()
            print('My')

    def insert_to_mongo(self):
        print('储存数据库中。。。')
        while True:
            if len(self.data_list) == 0:
                break
            insert(self.data_list.pop(),self.dbname)
            # print('Mo')

    def parse_info(self,page):
        '''
        将数据生成字典再保存进self.data_list里
        :param page: 传进页数
        :return: None
        '''
        url='https://api.bilibili.com/archive_rank/getarchiverankbypartion?jsonp=jsonp&tid={tid}&pn={page}'.format(tid=self.tid,page=page)
        headers={}
        response=requests.get(url,headers=headers,timeout=5)
        json_=json.loads(response.text)
        archives=json_['data']['archives']
        for i in archives:
            data = {}
            #上层信息
            data['author']=i['author']#up名字
            data['create'] = i['create']#上传时间
            data['play'] = i['play']#播放量
            data['title'] = i['title']#视频标题
            data['video_review'] = i['video_review']#评论数目
            # 下层信息
            data['aid'] = i['stat']['aid']#视频av号
            data['coin'] = i['stat']['coin']#硬币
            data['favorite'] = i['stat']['favorite']#收藏
            data['danmaku'] = i['stat']['danmaku']#弹幕数量
            data['like'] = i['stat']['like']#喜欢
            data['dislike'] = i['stat']['dislike']#rua鸡
            data['his_rank'] = i['stat']['his_rank']#历史排行
            data['now_rank'] = i['stat']['now_rank']#如今排行
            data['reply'] = i['stat']['reply']#回复数量
            data['share'] = i['stat']['share']#分享数量
            data['view'] = i['stat']['view']#播放数量
            # print(data)
            self.data_list.append(data)

    def max_page(self):
        '''
        :return: 视频总页数
        '''
        url='https://api.bilibili.com/archive_rank/getarchiverankbypartion?jsonp=jsonp&tid={tid}&pn={page}'.format(tid=self.tid,page=1)
        headers={}
        response=requests.get(url,headers=headers)
        json_=json.loads(response.text)
        count=json_["data"]["page"]["count"]
        if int(count)%20==0:
            max_page=int(int(count) / 20)
        else:
            max_page = int(int(count) / 20)+1
        self.max=max_page

    def num_in_queue(self):
        '''
        把页数put进Queue里
        :return: None
        '''
        # 获取总页数
        self.max_page()
        print('Total pages {}'.format(self.max))
        for i in range(1,self.max):
            self.page_list.put(i)

    def scheduler(self):
        '''
        每从Queue里取1000个页面，就执行一次存数据操作；
        :return:
        '''
        self.count+=1
        # 修改线程数量：
        pool = ThreadPoolExecutor(max_workers=12)
        th=0
        # 修改爬取-储存间隔：
        epart = 500

        if int(self.max) >epart:
            part=epart
        else:
            part=int(int(self.max)/2)
        print('{}*{}'.format(self.count,part))
        while self.page_list.qsize() > 0:
            th+=1

            if th ==part+1:
                break
            else:
                pool.submit(self.parse_info, self.page_list.get())

        pool.shutdown()
        #可供选择的两个数据库：

        #开启的是Mysql数据库：
        # self.insert_to_mysql()

        #开启的是Mongodb数据库：
        self.insert_to_mongo()

    def run(self):
        self.num_in_queue()
        while self.page_list.qsize() > 0:
            self.scheduler()

if __name__ == '__main__':
    time_start=time.time()
    #填写视频分区编号：
    tid=86
    # 填写数据库名字：
    db_name='影视-特摄'

    M=Mbilibili(tid,db_name)
    M.run()

    time_end = time.time()
    print('Toatl time {}'.format(time_end-time_start))