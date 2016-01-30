import UserDict

try:
    import cPickle as pickle
except ImportError:
    import pickle

"""
put pickle objects into a database table

table
key:string
value:text

"""
class PgShelve(UserDict.DictMixin):
    def __init__(self, conn, table, name):
        self.conn = conn
        self.table = table
        self.name = name
        self.dict = self.getRemoteData()

    def getRemoteData(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM "+self.table+" WHERE KEY = %s", (self.name,))
        data = cur.fetchone()
        try: return pickle.loads(str(data[2]))
        except TypeError: return {}

    def rowExists(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM "+self.table+" WHERE KEY = %s", (self.name,))
        return cur.fetchone()[0] == 1

    def persistData(self, dict):
        cur = self.conn.cursor()
        if self.rowExists():
            cur.execute("UPDATE "+self.table+" SET VALUE = %s WHERE KEY = %s", (pickle.dumps(self.dict), self.name,))
        else:
            cur.execute("INSERT INTO "+self.table+" (KEY, VALUE) VALUES (%s, %s)", (self.name, pickle.dumps(self.dict),))
        self.conn.commit()

    def __setitem__(self, key, item): self.dict[key] = item

    def __getitem__(self, key): return self.dict[key]

    def keys(self): return self.dict.keys()

    def sync(self):
        self.persistData(self.dict)

if __name__ == "__main__":
    import psycopg2
    conn = psycopg2.connect(open('db.conf').read())
    ps = PgShelve(conn, "pgshelve", "main")
    ps["foo"] = ["bar", "baz", {"zzzz": 1.22}]
    assert "foo" in ps
    ps.sync()

    ps = PgShelve(conn, "pgshelve", "main")
    assert "foo" in ps
