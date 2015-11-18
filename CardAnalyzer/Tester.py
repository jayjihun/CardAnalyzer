from TransactionDB import *
a = Record.Record(2015,11,19,3,52,5,10000)
print(a)

db = TransactionDB()

db.insertRecord(a)

db.printAllRecords()