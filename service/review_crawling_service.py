import pymysql


class Review_crawling_service:
    conn = None
    host = "alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com"
    user = "root"
    password = "1q2w3e4r!"
    database = "alpha"

    def __init__(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    charset='utf8')

    def save(self, review_crawling):
        self.conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                               user='root',
                               password='1q2w3e4r!',
                               db='alpha',
                               charset='utf8')

        sql = "insert into " \
              "review_crawling(`restaurant_id`, `content`, `report`, `writer`, `writedttm`) " \
              "values(%s, %s, %s, %s, %s)"
        val = (review_crawling.restaurant.id, review_crawling.content, review_crawling.report, review_crawling.writer,
               review_crawling.writedttm)

        with self.conn:
            with self.conn.cursor() as cur:
                if val:
                    cur.execute(sql, val)
                else:
                    cur.execute(sql)
                self.conn.commit()
                return cur.lastrowid
        return None
