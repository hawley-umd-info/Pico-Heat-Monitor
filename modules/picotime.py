"""
Author: dev.slife
Date Created: 2/18/26
Date Updated: 6/17/26
Description: Handles local time and date information.
"""


# ---------------------- IMPORT MODULES ---------------------- #

from .piconet import http_request
from .config import REPORTING_TIMES


# ------------------------ CONSTANTS ------------------------ #

# Month mapping
MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]



# ----------------------- GRAB LOCAL TIME ----------------------- #

def fetchTime():
    """
    Grabs the local time from the TIMESERVER.
    
    Returns:
        A tuple consisting of the date and time with the format: [Y, D, M, Hr, Min, Sec]
        
    Side effects:
        Prints any OSErrors that were caught to the terminal
    """
    try:
        response_json = http_request()
        if response_json:
            curDate = response_json["date"].split("-")
            curTime = response_json["time"].split(":")
            curTime[-1] = curTime[-1].split(".")[0]
            dateTime = curDate + curTime
            result = tuple([dt for dt in dateTime])
            return result
    except OSError as e:
        print(f"An {type(e).__name__} occurred: {e}")



# ------------------------ LOCAL CLOCK ------------------------ #

class PicoClock:
    """
    The Pico's internal clock.
    
    Attributes:
        date (str) - the current date
        time (str) - the current time
        timestamp (str) - the current timestamp
    """
    
    def __init__(self, timeStamp:tuple=None, sync:bool=True):
        if (sync and not timeStamp):
            self.sync()
        else:
            self.__process(timeStamp)
          
      
    def __process(self, timeStamp:tuple):
        """
        Processes the given timestamp.
        
        Args:
            timeStamp (tuple) - The given timestamp ordered: [Y, D, M, Hr, Min, Sec]
            
        Side effects:
            Updates the 'private' processed attribute of the current object.
        """
        if (timeStamp):
            self.__processed = {
                "Y": timeStamp[0],
                "D": timeStamp[1],
                "M": timeStamp[2],
                "Hr": timeStamp[3],
                "Min": timeStamp[4],
                "Sec": timeStamp[5]
            }
            self.date = "-".join(timeStamp[:3])
            self.time = ":".join(timeStamp[3:])
            self.timestamp = f"{self.date}|{self.time}"
        else:
            self.__processed = None
            self.date = None
            self.time = None
            self.timestamp = None
        
        
    def sync(self):
        """
        Syncs the Pico's clock with the TIMESERVER.
        
        Side effects:
            Updates the current object
        """
        self.__process(fetchTime())
        
        
    def update(self, curDate:str, curTime:str):
        """
        Updates the clock to represent the new timestamp.
        
        Args:
            curDate (str) - The given current date
            curTime (str) 0 The given current time
            
        Returns:
            The updated timestamp
        """
        if (curDate and curTime):
            self.__process(curDate.split("-") + curTime.split(":"))
        elif (self.__processed):
            if (curDate):
                self.__process(curDate.split("-") + [
                    self.__processed["Hr"],
                    self.__processed["Min"],
                    self.__processed["Sec"]
                ])
            elif (curTime):
                self.__process([
                    self.__processed["Y"],
                    self.__processed["D"],
                    self.__processed["M"],
                ] + curTime.split(":"))
            else:
                print("WARNING: Could not update timestamp due to no time and/or date given.")
        else:
            print("WARNING: Could not update timestamp due to desynced clock.")
        

    def inc_time(self, incType:str='s', amount:int=1):
        """
        Locally increments the time, so network communication isn't needed.
        
        Args:
            incType (str) - The type to increment:
                - 'h' for hour
                - 'm' for minute
                - 's' for second
            amount (int) - The amount to increment by
            
        Returns:
            The new incremented time
        """
        if (not self.time):
            return "Unknown"
        elif (incType in ['h', 'm', 's']):
            h, m, s, = map(int, self.time.split(":"))
            
            # increment
            s = s+amount if incType == 's' else s
            m = m+amount if incType == 'm' else m
            h = h+amount if incType == 'h' else h
            
            # update values to be in proper format
            while (s >= 60 or m >= 60 or h >= 24):
                if (s >= 60):
                    m = m+1
                    s = s-60
                if (m >= 60):
                    h = h+1
                    m = m-60
                if (h >= 24):
                    h = 0
                    m = 0
                    s = 0
            
            # return values and update clock
            newTime = f"{h:02d}:{m:02d}:{s:02d}"
            self.update(None, newTime)
            return newTime
        else:
            print("WARNING: could not increment given time; invalid incType given.")



# ----------------------- FORMATTING ----------------------- #

def format_MonthDDYr(m: int, d: int, y: int) -> str:
    """
    Formats a date in Month DD Yr
    
    Args:
        m (int) - the given month number
        d (int) - the given day
        y (int) - the given year
        
    Returns:
        The date in the Month DD Yr format
    """
    return f"{MONTHS[m - 1]} {d:02d} {y}"


def format_MMDDYY(date=None, m=None, d=None, y=None):
    """
    Formats a date in MM/DD/YY.
    
    Args:
        m (str) - the given month name
        d (int) - the given day
        y (int) - the given year
        
    Returns:
        The date in the MM/DD/YY format
    """
    if (date and date == "Unknown"):
        return "Unknown"
    elif (date and isinstance(date, str)):
        m, d, y = date.split(" ")
    
    if (m and d and y):
        return f"{MONTHS.index(m)}/{int(d):02d}/{str(y)[2:]}"
    else:
        print("WARNING: Date could not be properly formatted.")



# ----------------------- REPORTING TIME ----------------------- #

def isTimeToReport(t) -> bool:
    """
    Checks if it's time to report the data.
    
    Args:
        t (str) - the time to check [format "00:00:00"]
    
    Returns:
        A boolean result of true if the time matches and false otherwise.
    """
    if (t != "Unknown"):
        t_h, t_m, _, = map(int, t.split(":"))
        
        for reporttime in REPORTING_TIMES:
            rt_h, rt_m, _, = map(int, reporttime.split(":"))
            if t_h == rt_h and t_m == rt_m:
                return True

    return False