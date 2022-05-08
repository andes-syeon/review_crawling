import pymysql


class Pymysql:
    conn = None
    host = "alpha-project-db2.ctv6svlo10hb.us-east-1.rds.amazonaws.com"
    user = "root"
    password = "1q2w3e4r!"
    database = "alpha"

    def __init__(self):
        return

    def execute(self, sql, val=None):
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
                return cur.fetchall()
        return None

    def execute_one(self, sql, val=None):
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
                return cur.fetchone()
        return None

    def insert(self, sql, val=None):
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


def main():
    conn = Pymysql()

    sql = "select * from restaurant"

    data = conn.execute(sql)
    print(data)


if __name__ == "__main__":
    main()
