import UserDict
import traceback

try:
    import cPickle as pickle
except ImportError:
    import pickle

class PgShelve(UserDict.DictMixin):
    def __init__(self, conn):
        self.conn = conn
        self.dict = self.fetch()

    def fetch(self):
        dict = {}
        cur = self.conn.cursor()
        cur.execute("SELECT URL,STATE FROM PAGES")
        for row in cur.fetchall():
            dict[row[0]] = pickle.loads(str(row[1]))
        return dict

    def keyExists(self, key, cur):
        cur.execute("SELECT COUNT(*) FROM PAGES WHERE URL = %s", (key,))
        return cur.fetchone()[0] == 1

    def commit(self):
        cur = self.conn.cursor()
        for key in self.dict:
            val = pickle.dumps(self.dict[key])
            if self.keyExists(key, cur):
                cur.execute("UPDATE PAGES SET STATE = %s WHERE URL = %s", (val, key,))
            else:
                cur.execute("INSERT INTO PAGES (URL, STATE) VALUES (%s, %s)", (key, val,))
        self.conn.commit()

    def __setitem__(self, key, item):
        self.dict[key] = item

    def __getitem__(self, key):
        return self.dict[key]

    def keys(self):
        return self.dict.keys()

    def sync(self):
        self.commit()

if __name__ == "__main__":
    import psycopg2
    conn = psycopg2.connect(open('db.conf').read())
    ps = PgShelve(conn)
    ps["foo"] = (True, 2)
    assert "foo" in ps
    ps.sync()

    ps = PgShelve(conn)
    assert "foo" in ps
