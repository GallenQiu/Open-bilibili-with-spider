                   
Bilibili视频信息爬虫
===========================

###########环境依赖

            python3
            依赖库：requests、ThreadPoolExecutor、Queue、DBUtils.PooledDB、pymongo、mysql.connector
            MongoDB/Mysql

###########操作步骤

            1. 查找视频分区对应编号tid：
                        运行 查询分区编号.py 即可得到对应编号和信息


            2. 配置run.py文件：
                        将tid和mongodb集合的名字填进对应位置：Main函数里

            3. 运行run.py

            4. 相关修改：（均在run.py文件中修改）
                1、多线程数量
                2、爬取和存储间隔


###########目录结构描述

            ├── Readme.md                   // help
            ├── run.py                         // 爬虫核心
            ├── mbi_Mysql.py                    // Mysql数据库配置文档
            ├── mbi_Mongo.py                    // Mongo数据库配置文档
            ├── 查询分区编号.py                         // 查询分区编号文档
            ├── 分类.json           // tid的json文件
            ├── 参数对照表.xlsx              // 视频参数对照
            └── 


###########V1.0.0 版本内容更新
1. 功能     获取：

            视频id
            up主名字
            是否自制
            上传时间
            短简介
            动态介绍
            up头像
            收藏数量
            封面图
            播放
            分类编号
            标题
            分类名字
            视频评论
            视频数量
            界面规格
            播放设置
            视频数据
            视频id
            硬币
            弹幕数量
            不喜欢数量
            收藏
            历史最高排行
            喜欢数量
            现在排行
            回复数量
            分享数量
            观看数量

