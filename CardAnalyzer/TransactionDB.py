import sqlite3
import Record



init_query = '''CREATE TABLE IF NOT EXISTS transactions(
year int,
month int,
day int,
hour int,
minute int,
second int,
price int,
card text,
method text,
place text,
primary key(year,month,day,hour,minute,second,price)
);
'''

class TransactionDB(object):
    '''sqlite3 wrapper class. contains records'''
    def __init__(self, dbpath='C:/pythonplay/transactions.db'):
        self.con = sqlite3.connect(dbpath, detect_types = sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()
        self.cur.execute(init_query)
    
    def __del__(self):
        self.con.commit()
        self.con.close()    
    
    def insertRecord(self, record):
        try:
            self.cur.execute('INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?);',record.decompose())
        except:
            pass

    def replaceRecord(self, record):
        try:
            self.cur.execute('REPLACE INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?);',record.decompose())
        except:
            pass

    def selectRecord(self, query='SELECT * FROM transactions;'):
        self.cur.execute(query)
        result = self.cur.fetchall()
        try:
            finalresult = [Record.Record.initFromTuple(data) for data in result]
        except:
            finalresult = result
        return finalresult

    def getAllRecords(self):
        return self.selectRecord()

    def printAllRecords(self):
        records = self.getAllRecords()
        for record in records:
            print(record)
        print('Total num :',len(records))