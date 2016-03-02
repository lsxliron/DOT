import datetime
from models import *

def parseDate(d):
    """
    Parse a date in format mm-dd-yyyy
    
    Parameters
    ----------
        d : str
            The date to parse

    Return
    ------
        datetime.date
    """

    if d.count('-')!=2:
        return "Invalid date format. Please enter date as mm-dd-yyyy"

    tempDate = d.split('-')
    if len(tempDate)!=3:
        return "Invalid Date"
    
    try:
        return datetime.date(int(tempDate[2]), int(tempDate[0]), int(tempDate[1]))

    except ValueError as e:
        return"Date error, " + str(e)
        



def parseTime(t):
    """
    Parse a timestamp in format HH:MM:SS

    Parameters
    ----------
        t : str
            The time to parse
    Return
    ------
        datetime.time
    """

    if t.count(':')!=2:
        return"Invalid time format. Please enter time as hh:mm:ss"

    tempTime = t.split(':')
    if len(tempTime)  != 3:
        return "Invlaid time"
    
    try:
        return datetime.time(int(tempTime[0]), int(tempTime[1]), int(tempTime[2]))
    except ValueError as e:
        return "Time error, " + str(e)


def getDates(startDate, endDate):

    if startDate and not endDate:
        return "Missing end date"

    elif endDate and not startDate:
        return "Missing start date"
    
    elif startDate and endDate:
        startDate = parseDate(startDate)
        endDate = parseDate(endDate)

        #MAKE SURE DELTA IS POSITIVE
        if (endDate - startDate).total_seconds() < 0:
            return "End date cannot be before start date"

    return [startDate, endDate]


def getTimes(startTime, endTime):
    if startTime and not endTime:
        return"Missing end time"
        

    elif endTime and not startTime:
        return "Missing start time"

    elif endTime and startTime:
        startTime = parseTime(startTime)
        endTime = parseTime(endTime)
            
        #MAKE SURE DELTA IS POSITIVE
        tempStartTime = datetime.timedelta(startTime.hour, startTime.minute, startTime.second)
        tempEndTime = datetime.timedelta(endTime.hour, endTime.minute, endTime.second)
        if (tempEndTime - tempStartTime).total_seconds() < 0:
            return "End time cannot be before start time"

    return [startTime, endTime]


def getResults(db, startDate=None, endDate=None, startTime=None, endTime=None, 
               location=None, rain=None, lim=None):
    result = db.session.query(DotImage)
    if startDate and endDate:
        result = result.filter(DotImage.date > startDate).filter(DotImage.date < endDate)

    if startTime and endTime:
        result = result.filter(DotImage.time > startTime).filter(DotImage.time < endTime)

    if rain == 0 or rain == 1:
        result = result.filter(DotImage.rain == rain)

    if location:
        result = result.filter(DotImage.locationId == location)

    if lim:
        result = result.limit(lim)
    return result