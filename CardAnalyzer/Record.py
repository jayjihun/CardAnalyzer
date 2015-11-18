class Record:
    def __init__(self, year, month, day, hour, minute, second, price=0, card = '모르는', method = '체크', place = '모름'):
        self.year, self.month, self.day, self.hour, self.minute, self.second = year,month,day,hour,minute,second
        self.price, self.card, self.method, self.place = price, card, method, place

    @classmethod
    def initFromTuple(cls,a):
        return cls(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9])

    def __repr__(self):
        return "Record(%d년 %d월 %d일 %d시 %d분 %d초, %d원 %s카드 %s로 %s에서)"%(self.year,self.month,self.day,self.hour,self.minute,self.second,self.price,self.card,self.method,self.place)

    def decompose(self):
        return (self.year,self.month,self.day,self.hour,self.minute,self.second,self.price,self.card,self.method,self.place)
