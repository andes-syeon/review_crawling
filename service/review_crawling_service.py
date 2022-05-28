import mysql_connector


class Review_crawling_service:
    conn = None

    def __init__(self):
        self.conn = mysql_connector.pymysql()

    def save(self, review_crawling):
        sql = "insert into " \
              "review_crawling(`restaurant_id`, `content`, `report`, `writer`, `writedttm`) " \
              "values(%s, %s, %s, %s, %s)"
        val = (review_crawling.restaurant.id, review_crawling.content, review_crawling.report, review_crawling.writer, review_crawling.writedttm)
        result = self.conn.insert(sql, val)
        return result
