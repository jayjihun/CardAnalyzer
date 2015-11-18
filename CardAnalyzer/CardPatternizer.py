# -*- coding: utf-8 -*-
import ExcelReader
import TransactionDB
import Analyzer

class Patternizer(object):
    def __init__(self, dbpath='C:/pythonplay/transactions.db'):
        self.db = TransactionDB.TransactionDB(dbpath)
        self.analyzer = Analyzer.Analyzer(self.db)

    def importFile(self, fname = 'C:/pythonplay/banks/2013 nong.xls'):
        reader = ExcelReader.Importer(self.db, fname)
        reader.read()
        reader.store()

    def getTransactionNumber(self):
        a = self.db.selectRecord('SELECT count(*) from transactions;')
        return a[0][0]
    
def main():
    robot = Patternizer()
    robot.importFile()
    print(robot.getTransactionNumber())


if __name__ == '__main__':
    main()