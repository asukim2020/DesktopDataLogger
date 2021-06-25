import time
import datetime as dt


class TimeUtil:

    @classmethod
    def getNewTimeByLong(cls):
        return TimeUtil.timeToLong(time.time())

    @classmethod
    def getNewDate(cls):
        t = time.time()
        date = dt.datetime.fromtimestamp(t)
        return date.replace(microsecond=0)

    @classmethod
    def timeToLong(cls, t):
        return int(t * 1000) % 0x10000000000000000

    @classmethod
    def longToDate(cls, t):
        date = TimeUtil.timeToDate(t / 1000)
        return date.replace(microsecond=0)

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

    @classmethod
    def getNextDay(cls, time, day):
        date = TimeUtil.longToDate(time)
        date += dt.timedelta(days=day)
        return date

    count = 0

    @classmethod
    def checkAClock(cls, maxMin):
        # TODO: - 테스트 코드 지울 것
        TimeUtil.count += 1
        if 3000 < TimeUtil.count < 6000:
            return True
        else:
            return False
        t = TimeUtil.getNewTimeByLong()
        min = (t % 3600000) / 60000
        if 0 <= min <= maxMin:
            return True
        else:
            return False

# test
if __name__ == "__main__":
    # date = TimeUtil.getDate(2021, 6, 24)
    # print(TimeUtil.dateToLong(date))
    print(TimeUtil.getDate(2021, 6, 24))


