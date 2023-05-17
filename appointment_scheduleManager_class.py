#Class to manage events/manage schedules
#Yet to be written, tested, and implemented
#Stores all dates that have been taken/ scheduled with their metadata (event_dates.txt)

import datetime
from datetime import datetime
import os
import json

class ScheduleManager:
    list_holiday_dates_23_24 = {
        {
         "Event Type": "Holiday", 
         "Event Name": "American Independence Day", 
         "Event Date" : "07/04/2023", 
         "Event Start Time": "00:00", 
         "Event End Time": "24:00", 
         "Event Description": "Federal Holiday - American Independence Day", 
         "Number of Participants":  "0", 
         "Participant Names": "No Participants"
        },
        {
         "Event Type": "Holiday", 
         "Event Name": "Mandatory Staff Development Day", 
         "Event Date" : "08/08/2023", 
         "Event Start Time": "00:00", 
         "Event End Time": "24:00", 
         "Event Description": "School Holiday - Mandatory Staff Development Day", 
         "Number of Participants":  "0", 
         "Participant Names": "No Participants"
        },
        {
         "Event Type": "Holiday", 
         "Event Name": "Mandatory Staff Development Day", 
         "Event Date" : "08/08/2023", 
         "Event Start Time": "00:00", 
         "Event End Time": "24:00", 
         "Event Description": "School Holiday - Mandatory Staff Development Day", 
         "Number of Participants":  "0", 
         "Participant Names": "No Participants"
        },
        "09/04/2023", #Labor Day
        "11/01/2023", #Mandatory Staff Development Day
        "11/10/2023", #Veteran's Day
        "11/17/2023", #PK-5 Student Non-Attendence/Teacher Conf/Work Day
        "11/20/2023", #Thanksgiving Break
        "11/21/2023", #Thanksgiving Break
        "11/22/2023", #Thanksgiving Break
        "11/23/2023", #Thanksgiving Break
        "11/24/2023", #Thanksgiving Break
        "12/20/2023", #HS Sem 1 Finals
        "12/21/2023", #HS Sem 1 Finals
        "12/22/2023", #HS Sem 1 Finals
        "12/25/2023", #Winter Break
        "12/26/2023", #Winter Break
        "12/27/2023", #Winter Break
        "12/28/2023", #Winter Break
        "12/29/2023", #Winter Break
        "12/30/2023", #Winter Break
        "12/31/2023", #Winter Break
        "01/01/2024", #Winter Break
        "01/02/2024", #Winter Break
        "01/03/2024", #Winter Break
        "01/04/2024", #Winter Break
        "01/05/2024", #Winter Break
        "01/08/2024", #Winter Break
        "01/09/2024", #6-12 Student Non-Attendance/Teacher Work Day
        "01/15/2024", #Martin Luther King Jr. Day
        "02/12/2024", #Lincoln's Day
        "02/19/2024", #President's Day
        "03/29/2024", #Spring Break
        "03/30/2024", #Spring Break
        "03/31/2024", #Spring Break
        "04/01/2024", #Spring Break
        "04/02/2024", #Spring Break
        "04/03/2024", #Spring Break
        "04/04/2024", #Spring Break
        "04/05/2024", #Spring Break
        "04/06/2024", #Spring Break
        "04/07/2024", #Spring Break
        "04/08/2024", #Spring Break
        "05/27/2024", #Memorial Day
        "05/29/2024", #HS Sem 2 Finals
        "05/30/2024", #HS Sem 2 Finals
        "05/31/2024", #HS Sem 2 Finals / End of Instructional Year
        "06/03/2024", #Mandatory Staff Development Day
    }

    instructionalYearStart = "08/10/2023"
    instructionalYearEnd = "05/31/2024"

    def __init__(cls):
        ScheduleManager.blockAllHolidayDates()

    @classmethod #method that writes the dates to be "scheduled/ignored" to the event_dates.txt file that stores all the scheduled dates
    def blockAllHolidayDates(cls):
        with open("Community_Planner/event_dates.txt", "a") as f:
            if os.path.getsize('Community_Planner/event_dates.txt') == 0:
                f.write("{}".format(datetime.date(datetime.strptime(ScheduleManager.instructionalYearStart, '%m/%d/%Y'))) + ", Holiday" + "\n")
                f.write("{}".format(datetime.date(datetime.strptime(ScheduleManager.instructionalYearEnd, '%m/%d/%Y'))) + ", Holiday" + "\n")
                for x in ScheduleManager.list_holiday_dates_23_24:
                    f.write("{}".format(datetime.date(datetime.strptime(x, '%m/%d/%Y'))) + ", Holiday" + "\n")
            else:
                pass
        f.close()

    @classmethod #verifies if a date passed into the function as a parameter is already "scheduled" (i.e exists in the event_dates.txt file)
    def checkIfDateBlocked(cls, proposedDate, dateType):
        with open("Community_Planner/event_dates.txt", "r") as a:
            if os.path.getsize('Community_Planner/event_dates.txt') != 0:
                eventContent = a.readlines()
                for x in eventContent:
                    if x.find(proposedDate) != -1:
                        return True
                return False
        a.close()
    
    @classmethod #gets the line number in the event_dates.txt of a specific date passed in (for data analysis purposes)
    def getIndexOfDate(cls, proposedDate, dateType):
        with open("Community_Planner/event_dates.txt", "r") as a:
            if os.path.getsize('Community_Planner/event_dates.txt') != 0:
                eventContent = a.readlines()
                for x in eventContent:
                    if (x.find(proposedDate) != -1):
                        return eventContent.index(x)
                return -1
        a.close()
    
    @classmethod #blocks(schedules) a date with the date and type passed in (type meaning a classifier denoting holiday, school event, etc.)
    def blockDate(cls, dateToBlock, dateType):
        with open("Community_Planner/event_dates.txt", "a") as a:
            a.write("\n" + "{}".format(datetime.date(datetime.strptime(dateToBlock, '%m/%d/%Y'))) + f", {dateType}")
        a.close()
    
    @classmethod  #unblock a date passed in (i.e remove it from the event_dates.txt file which stores all the dates that are "scheduled")
    def unblockDate(cls, dateToUnblock):
        with open("Community_Planner/event_dates.txt", "r+") as a:
            x = a.readlines()
            a.seek(0)
            for i in x:
                if i.find(dateToUnblock) == -1:
                    a.write(i)
            a.truncate()
    




