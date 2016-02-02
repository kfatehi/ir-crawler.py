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
            key = row[0]
            try:
                dict[key] = pickle.loads(str(row[1]))
            except pickle.UnpicklingError:
                # False as first value makes crawler add it to frontier
                dict[key] = (False, 0)
        cur.close()
        return dict

    def keyExists(self, key, cur):
        cur.execute("SELECT COUNT(*) FROM PAGES WHERE URL = %s", (key,))
        return cur.fetchone()[0] == 1

    def __setitem__(self, key, item):
        self.dict[key] = item
        cur = self.conn.cursor()
        val = pickle.dumps(self.dict[key])
        if self.keyExists(key, cur):
            cur.execute("UPDATE PAGES SET STATE = %s WHERE URL = %s", (val, key,))
        else:
            cur.execute("INSERT INTO PAGES (URL, STATE) VALUES (%s, %s)", (key, val,))
        self.conn.commit()
        cur.close()

    def __getitem__(self, key):
        return self.dict[key]

    def keys(self):
        return self.dict.keys()

    def sync(self):
        pass

if __name__ == "__main__":
    import psycopg2
    conn = psycopg2.connect(open('db.conf').read())
    ps = PgShelve(conn)
    ps["foo"] = (True, 2)
    assert "foo" in ps
    ps.sync()

    ps = PgShelve(conn)
    assert "foo" in ps
