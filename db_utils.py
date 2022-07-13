from matplotlib import use
import psycopg2

class db_manager:
    def __init__(self,config):
        self.conn = psycopg2.connect(dbname= config['dbname'], user = config['user'], password = config['password'], host = config['host'])
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def add_row(self, chat_id, idea):
        self.cursor.execute("INSERT INTO ideas (chat_id, name) VALUES(%s,%s)",(chat_id,idea))
        self.conn.commit()

    def get_all(self, chat_id):
        self.cursor.execute("""SELECT * FROM ideas WHERE chat_id = %s;""",(str(chat_id),))
        records = self.cursor.fetchall()
        return records