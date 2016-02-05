#!/usr/bin/env python
import urllib
import os
import sys
import argparse
import datetime
import logging
import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

logger=None

def main():
    global logger
    
    loggerLevel = logging.DEBUG
    logger = initLog(loggerLevel)
    parser = argparse.ArgumentParser(description="Queries DOT database.")
    
    parser.add_argument('action', type=str, help="query or get", choices=['query', 'get'])
    parser.add_argument('--startDate', metavar="mm-dd-yyyy", type=str, help="Start date")
    parser.add_argument('--endDate', metavar="mm-dd-yyyy", type=str, help="End date")
    parser.add_argument('--startTime', metavar="hh:mm:ss", type=str, help="Start time")
    parser.add_argument('--endTime', metavar="hh:mm:ss", type=str, help="End time")
    parser.add_argument('--rain', metavar="0/1", type=int, help="Rain status: 0=not-rainy, 1=rainy")
    parser.add_argument('--location', metavar="loc_id", type=int, help="The locaion ID of the camera")
    parser.add_argument('--limit', metavar="int", type=int, help="Max. number of results")

    args = parser.parse_args()

    action = args.action
    rain = args.rain
    location = args.location
    lim = args.limit

    #PARSE DATES AND TIMES
    startDate, endDate = getDates(args.startDate, args.endDate)
    startTime, endTime = getTimes(args.startTime, args.endTime)

    #PARSE RAIN
    if rain and rain!=0 and rain!=1:
        logger.error("Please choose a valid value for rain: 0 for non-rainy, 1 for rainy")

    #PARSE LOCATION
    if location:
        try:
            location = int(location)
        except ValueError:
            logger.error("Location must be an integer")
            sys.exit(-1)

    #PARSE LIMIT
    if lim:
        try:
            lim = int(lim)
        except ValueError:
            logger.error("Max number of results must be an integer")
            sys.exit(-1)


    #Connect to db
    engine = create_engine("sqlite:///" + settings.dbName, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    result = getResults(session, startDate, endDate, startTime, endTime, location, rain, lim)


    # PRINT IMAGES
    if action == 'query':
        printResults(result)

    # DOWNLOAD IMAGES
    else:
        path = os.path.dirname(os.path.abspath(__file__)) + '/img'

        if not os.path.exists(path):
            os.makedirs(path)

        for row in result:
            print 'downloading image {x}.jpg'.format(x=row.id)
            urllib.urlretrieve('http://localhost:8000' + row.path, path + '/' + str(row.id) + ".jpg")



def printResults(result):
    print "\nFound {n} results\n".format(n=result.count())
    print "|\tID\t|  Location\t|\tDate\t\t|\tTime\t\t|\tRain\t|"
    print "-" * 97
    for row in result:
        print "|\t{i}\t|\t{l}\t|\t{d}\t|\t{t}\t|\t{r}\t|".format(i=row.id, 
                                                                 l=row.locationId, 
                                                                 d=row.date, 
                                                                 t=row.time, 
                                                                 r=row.rain)


def getResults(session, startDate=None, endDate=None, startTime=None, endTime=None, 
               location=None, rain=None, lim=None):
    result = session.query(DotImage)
    if startDate and endDate:
        result = result.filter(DotImage.date > startDate).filter(DotImage.date < endDate)

    if startTime and endTime:
        result = result.filter(DotImage.time > startTime).filter(DotImage.time < endTime)

    if rain:
        result = result.filter(DotImage.rain == rain)

    if location:
        result = result.filter(DotImage.locationId == location)

    if lim:
        result = result.limit(lim)
    return result


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
        logger.error("Invalid date format. Please enter date as mm-dd-yyyy")
        sys.exit(-1)

    tempDate = d.split('-')
    if len(tempDate)!=3:
        logger.error("Invalid Date")
        sys.exit(-1)

    
    try:
        finalDate = datetime.date(int(tempDate[2]), int(tempDate[0]), int(tempDate[1]))

        #MAKE SURE YEAR > 1900
        if finalDate.year<=1900:
            logger.error("date cannot be before 01-01-1900")
            sys.exit(-1)
        return finalDate
        
    except ValueError as e:
        logger.error("Date error, " + str(e))
        sys.exit(-1)
        



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
        logger.error("Invalid time format. Please enter time as hh:mm:ss")
        sys.exit(-1)

    tempTime = t.split(':')
    if len(tempTime)  != 3:
        logger.error("Invlaid time")
        sys.exit(-1)
    
    try:
        finalTime = datetime.time(int(tempTime[0]), int(tempTime[1]), int(tempTime[2]))
        return finalTime
    except ValueError as e:
        logger.error(("Time error, " + str(e)))
        sys.exit(-1)



def initLog(loggerLevel):
    """
    Initialize the logger for the script.

    Parameters
    ----------
        loggerLevel: const
            The logger level. Can get the following values:
                - logging.DEBUG
                - logging.INFO
                - logging.WARINING
                - logging.CRITICAL
                - logging.ERROR

    Return
    ------
        logging.Logger

    """
    logger = logging.getLogger('DOT.py')
    logger.setLevel(loggerLevel)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def getDates(startDate, endDate):

    if startDate and not endDate:
        logger.error("Missing end date")
        sys.exit(-1)

    elif endDate and not startDate:
        logger.error("Missing start date")
        sys.exit(-1)
    
    elif startDate and endDate:
        startDate = parseDate(startDate)
        endDate = parseDate(endDate)

        #MAKE SURE DELTA IS POSITIVE
        if (endDate - startDate).total_seconds() < 0:
            logger.error("End date cannot be before start date")
            sys.exit(-1)

    return [startDate, endDate]

def getTimes(startTime, endTime):
    if startTime and not endTime:
        logger.error("Missing end time")
        sys.exit(-1)

    elif endTime and not startTime:
        logger.error("Missing start time")
        sys.exit(-1)

    elif endTime and startTime:
        startTime = parseTime(startTime)
        endTime = parseTime(endTime)
            
        #MAKE SURE DELTA IS POSITIVE
        tempStartTime = datetime.timedelta(startTime.hour, startTime.minute, startTime.second)
        tempEndTime = datetime.timedelta(endTime.hour, endTime.minute, endTime.second)
        if (tempEndTime - tempStartTime).total_seconds() < 0:
            logger.error("End time cannot be before start time")
            sys.exit(-1)
    return [startTime, endTime]

if __name__ == "__main__":
    main()
