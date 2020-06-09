from time import mktime
from datetime import datetime
import unicodedata

year = str(datetime.utcnow().year)


def translateString(string):
    return unicodedata.normalize('NFKD', string).encode()

def isSame(a, b, c):
    if a in b or b in a or a in c or c in a:
        return True

def _monthToNumber(m):
    if isSame(m, "janar", "january"):
        return 1
    elif isSame(m, "shkurt", "february"):
        return 2
    elif isSame(m, "mars", "march"):
        return 3
    elif isSame(m, "prill", "april"):
        return 4
    elif isSame(m, "maj", "may"):
        return 5
    elif isSame(m, "qershor", "june"):
        return 6
    elif isSame(m, "korrik", "july"):
        return 7
    elif isSame(m, "gusht", "august"):
        return 8
    elif isSame(m, "shtator", "september"):
        return 9
    elif isSame(m, "tetor", "october"):
        return 10
    elif isSame(m, "ntor", "november"):
        return 11
    elif isSame(m, "dhjetor", "december"):
        return 12


def getTimeStamp(date, format):
    return mktime(datetime.strptime(date, format).timetuple())


def strSplit(string):
    if "," in string:
        return string.split(",")[0].strip(), string.split(",")[1].strip()
    else:
        return string.split(" ")[0].strip(), "2019"


def dateToTimeStamp(date):
    date = date.strip()
    format = "%d/%m/%Y %H:%M"

    month = _monthToNumber(''.join(i for i in date if i.isalpha()).strip().lower())
    date = ''.join(i for i in date if not i.isalpha()).strip()
    day, date = strSplit(date)

    try:
        _time = date.split(year)[1].strip()
    except:
        _time = "9:00"

    if _time != "9:00" and ":" not in _time:
        _time = "9:00"

    date = "{}/{}/{} {}".format(day, month, year, _time)
    date = getTimeStamp(date, format)
    return date
