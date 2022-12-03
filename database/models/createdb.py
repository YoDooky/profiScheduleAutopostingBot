import psycopg2
from config import db_config
from config.db_config import ADMINS_TABLE, POSTS_TABLE


class DbCreator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_config.DB_HOST,
            dbname=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            port=db_config.DB_PORT,
        )
        self.cursor = self.conn.cursor()

    def __create_admins_table(self):
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {ADMINS_TABLE} (
                            user_id bigint PRIMARY KEY
                            )""")

    def __create_posts_table(self):
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {POSTS_TABLE} (
                            id SERIAL PRIMARY KEY,
                            post_photo_id text,
                            post_text text,
                            schedule_period text,
                            schedule_time text
                            )""")

    def __init_db__(self):
        try:
            self.__create_admins_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create admins table\n'
                  f'[EX] {ex}')
        try:
            self.__create_posts_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create posts table\n'
                  f'[EX] {ex}')
