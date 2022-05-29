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
        sql = "select count(1)" \
              "from restaurant " \
              "where name = %s"
        val = (restaurant.name)

        if self.conn.execute_one(sql, val) == 0:
            return False
        else:
            return True

    def get_id(self, restaurant):
        sql = "select id " \
              "from restaurant " \
              "where name = %s"
        val = (restaurant.name)
        result = self.conn.execute_one(sql, val)
        if result:
            result = result[0]
        return result

    def save(self, restaurant):
        try:
            sql = "insert into " \
                  "restaurant(`original_name`, `name`, `address`, `local`, `operation`, `number`, `infodttm`, `star`, `regdttm`)" \
                  "values(%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
            val = restaurant.to_parentheses()
            result = self.conn.insert(sql, val)
            return result
        except Exception as e:
            print(e)
            return 0
