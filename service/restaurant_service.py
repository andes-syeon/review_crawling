import pymysql


class Restaurant_service:
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

    def is_exist(self, restaurant):
        self.conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                               user='root',
                               password='1q2w3e4r!',
                               db='alpha',
                               charset='utf8')
        sql = "select count(1)" \
              "from restaurant " \
              "where name = %s"
        val = (restaurant.name)

        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    charset='utf8')
        with self.conn:
            with self.conn.cursor() as cur:
                if val:
                    cur.execute(sql, val)
                else:
                    cur.execute(sql)
                if cur.fetchone() == 0:
                    return False
                else:
                    return True
        return False

    def get_id(self, restaurant):
        self.conn = pymysql.connect(host='alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com',
                               user='root',
                               password='1q2w3e4r!',
                               db='alpha',
                               charset='utf8')
        sql = "select id " \
              "from restaurant " \
              "where name = %s"
        val = (restaurant.name)

        with self.conn:
            with self.conn.cursor() as cur:
                if val:
                    cur.execute(sql, val)
                else:
                    cur.execute(sql)
                result = cur.fetchone()
                if result:
                    result = result[0]
                return result
        return None

    def save(self, restaurant):
        try:
            sql = "insert into " \
                  "restaurant(`original_name`, `name`, `address`, `local`, `operation`, `number`, `infodttm`, `star`, `regdttm`)" \
                  "values(%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
            val = restaurant.to_parentheses()

            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        database=self.database,
                                        charset='utf8')
            with self.conn:
                with self.conn.cursor() as cur:
                    if val:
                        cur.execute(sql, val)
                    else:
                        cur.execute(sql)
                    self.conn.commit()
                    return cur.lastrowid
            return None
        except Exception as e:
            print(e)
            return 0
