import Record
import xlrd
import re

nonghyupDic = {"날짜":2, "시간":2, "출금":3, "거래":6,"상호":7};

def extractFromCell(string):
    return (string.split(':',1)[-1]).replace("'","").replace("\\n"," ")

def getDates(string):
    try1 = '\d{4}-\d{2}-\d{2}'
    try2 = '\d{4}/\d{2}/\d{2}'
    a = re.search(try1,string)
    if a is not None:
        extracted = a.group()
        return int(extracted[0:4]), int(extracted[5:7]), int(extracted[8:10])
    a = re.search(try2,string)
    if a is not None:
        extracted = a.group()
        return int(extracted[0:4]), int(extracted[5:7]), int(extracted[8:10])


def getTimes(string):
    try1 = '[0-9]{2}:[0-9]{2}:[0-9]{2}'
    a = re.search(try1,string)
    if a is not None:
        extracted = a.group()
        return int(extracted[0:2]), int(extracted[3:5]), int(extracted[6:8])

def getPrice(string):
    string = string.replace('원','')
    string = string.replace(',','')
    return int(float(string))

def includeDate(string):
    try1 = '\d{4}-\d{2}-\d{2}'
    try2 = '\d{4}/\d{2}/\d{2}'
    if re.search(try1,string) is not None:
        return True;
    if re.search(try2,string) is not None:
        return True;
    return False;

def includeTime(string):
    try1 = '[0-9]{2}:[0-9]{2}:[0-9]{2}'
    if re.search(try1,string) is not None:
        return True
    return False

def includeDateOrTime(string):
    return includeDate(string) or includeTime(string)


class Importer(object):
    def __init__(self, db, fname='C:/pythonplay/banks/2013년 농협.xls'):
        self.workbook = xlrd.open_workbook(fname)
        self.sheets = list()
        self.db = db
        
       
    
    def read(self):
        for i in range(0,self.workbook._all_sheets_count):
            self.sheets.append(self.workbook.sheet_by_index(i))
            
    def listizeSheet(self,sheet):
        num_rows = sheet.nrows
        num_cols = sheet.ncols

        result = list()
        for row_index in range(0,num_rows):
            row = list()
            for col_index in range(0,num_cols):
                cell = sheet.cell(row_index,col_index)
                val = "%s"%(cell,)
                row.append(extractFromCell(val))
            result.append(row)
        return result




    def recordizeString(self, strings):
        #1. find first meaningful row.

        time_appearance = [0,]*len(strings[0])
        for i in range(0,min(len(strings),20)):
            for j in range(0,len(strings[0])):
                content = strings[i][j]
                if(includeDateOrTime(content)):
                    time_appearance[j] += 1

        max_index = 0
        max_appearance = 0
        for i in range(len(time_appearance)):
            if time_appearance[i] > max_appearance:
                max_index = i
                max_appearance = time_appearance[i]

        # i date/time column.
        legend = 0
        for i in reversed(range(0,min(len(strings),11))):
            if not includeDateOrTime(strings[i][max_index]):
                legend = i
                break
        del strings[0:legend]

        #what we have to figure out : 1.날짜 2.시간 3.출금금액 4.거래내용 5.상호명

        columnDic = nonghyupDic
        
        del strings[0:1]
        result = list()
        for string in strings:
            try:
                y,m,d = getDates(string[columnDic["날짜"]])
                h,mm,s = getTimes(string[columnDic["시간"]])
                p = getPrice(string[columnDic["출금"]])
                me = string[columnDic["거래"]]
                pla = string[columnDic["상호"]]
                if None in [y,m,d,h,mm,s,p,'농협',me,pla]:
                    continue
            except:
                continue
            rec = Record.Record(y,m,d,h,mm,s,p,'농협',me,pla)
            result.append(rec)

        return result



    def store(self):
        '''Perform conversion from .xls ===> List of strings ===> List of Meaningful Records'''
        #1. .xls => List of strings
        strings = list()
        for sheet in self.sheets:
            strings.extend(self.listizeSheet(sheet))
        '''
        a= 0
        for row in strings:
            a+=1
            print(row)
            if a is 50:
                break
           '''     
        #2. List of strings => List of Meaningful Records
        records = self.recordizeString(strings)
        '''
        a= 0
        for row in records:
            a+=1
            print(row)
            if a is 50:
                break
           '''

        #3. insert into the DB
        for record in records:
            self.db.replaceRecord(record)
