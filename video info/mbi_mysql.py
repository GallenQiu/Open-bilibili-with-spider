import mysql.connector
class db:
    def __init__(self,conn,item):
        self.conn=conn
        self.item=item

    def insert(self):
        cursor=self.conn.cursor()
        try:
            print('kaishi')
            cursor.execute(
                """insert into mbilibili_1(author,create_,play,title,video_review,aid,coin,favorite,danmaku,like_,dislike,his_rank,now_rank,reply,share,view_
)value(%s, %s, %s,%s,%s, %s, %s,%s,%s, %s, %s,%s,%s, %s, %s,%s)""",
                (
                    self.item['author'],
                    self.item['create'],
                    self.item['play'],
                    self.item['title'],
                    self.item['video_review'],
                    self.item['aid'],
                    self.item['coin'],
                    self.item['favorite'],
                    self.item['danmaku'],
                    self.item['like'],
                    self.item['dislike'],
                    self.item['his_rank'],
                    self.item['now_rank'],
                    self.item['reply'],
                    self.item['share'],
                    self.item['view']
                )
                )
        except mysql.connector.Error as e:
            print('Mysql error!{}'.format(e))
        finally:
            self.conn.commit()
            cursor.close()
            self.conn.close()
# if __name__ == '__main__':