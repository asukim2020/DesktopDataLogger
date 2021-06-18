import time
import datetime as dt


class TimeUtil:

    @classmethod
    def getNewTimeByLong(cls):
        return TimeUtil.timeToLong(time.time())

    @classmethod
    def timeToLong(cls, t):
        return int(t * 1000) % 0x10000000000000000

    @classmethod
    def LongToDate(cls, t):
        return TimeUtil.timeToDate(t / 1000)

    @classmethod
    def timeToDate(cls, t):
        return dt.datetime.fromtimestamp(t)

    @classmethod
    def dateToTime(cls, d):
        return d.timestamp()

    @classmethod
    def dateToLong(cls, d):
        t = TimeUtil.dateToTime(d)
        return TimeUtil.timeToLong(t)

    @classmethod
    def getDate(cls, year, month, day):
        dateString = ('%d-%d-%d' % (year, month, day))
        return dt.datetime.strptime(dateString, '%Y-%m-%d')

# test
if __name__ == "__main__":
    print(TimeUtil.getDate(2019, 8, 1))


