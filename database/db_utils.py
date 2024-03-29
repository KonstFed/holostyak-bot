import psycopg2
class db_manager:
    def __init__(self,config):
        self.conn = psycopg2.connect(dbname= config['dbname'], user = config['user'], password = config['password'], host = config['host'])
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def add_row(self, idea_name, author, description,season, timescooked = 0):
        self.cursor.execute("INSERT INTO ideas (name, author, description, season, timescooked) VALUES(%s,%s,%s,%s,%s)",(idea_name, author, description, season, timescooked))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("""SELECT * FROM ideas""")
        records = self.cursor.fetchall()
        return records

    def create_table(self, table_name):
        command = "CREATE TABLE " + table_name + \
        " (id SERIAL PRIMARY KEY, name text, author text, description text, season integer, timescooked integer)"
        self.cursor.execute(command)
        self.conn.commit()

    def get_last_id(self):
        self.cursor.execute("SELECT last_value FROM ideas_id_seq")
        return self.cursor.fetchall()[0][0]

    def change_row(self, id, idea_name, author, description, season, timescooked ):
        self.cursor.execute("UPDATE SET name = %s, author = %s, description = %s, season = %s, timescooked = %s WHERE id = %s" , (idea_name, author, description, season,timescooked, id))
        self.conn.commit()

    def delete_row(self, id):
        self.cursor.execute("DELETE FROM ideas WHERE id = %s",(id,))
        self.conn.commit()
    