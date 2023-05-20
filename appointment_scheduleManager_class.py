#Class to manage events/manage schedules
#Yet to be tested
#Stores all dates that have been taken/ scheduled with their metadata (event_dates.txt)

import datetime
from datetime import datetime
import os
import json
import pandas

#incorporates school instructional calendar

class ScheduleManager:
    def __init__(cls):
        ScheduleManager.blockAllHolidayDates()

    @classmethod #method that writes the dates to be "scheduled/ignored" to the event_dates.json file that stores all the scheduled dates
    def blockAllHolidayDates(cls):
        with open("Community_Planner/event_dates.json", "a") as f:
            if os.path.getsize("Community_Planner/event_dates.json") == 0:
                excel_holidays_xlsx = pandas.read_excel('Community_Planner/2023_2024_AVHS_InstructionalYearHolidays_CommunityEventPlanner.xlsx', sheet_name='event_dates', converters={"Event Date":str})
                excel_holidays_string = excel_holidays_xlsx.to_json(orient = 'records')
                excel_holidays_json = json.loads(excel_holidays_string)
                json.dump(excel_holidays_json, f)
            else:
                pass
        f.close()

    @classmethod #verifies if a date passed into the function as a parameter is already "scheduled" (i.e exists in the event_dates.txt file)
    def checkIfEventBlocked(cls, eventList):
        with open("Community_Planner/event_dates.json", "r") as a:
            if os.path.getsize('Community_Planner/event_dates.json') != 0:
                data = json.load(a)
                for x in data:
                    if (datetime.strptime(x.get("Event Date"), '%Y-%m-%d %H:%M:%S') == datetime.strptime(eventList["Event Date"],  '%Y-%m-%d %H:%M:%S')) and ((datetime.strptime(eventList["Event Start Time"], '%H:%M:%S') == datetime.strptime(x.get("Event Start Time"), '%H:%M:%S')) or (datetime.strptime(x.get("Event Start Time"), '%H:%M:%S') <= datetime.strptime(eventList["Event Start Time"], '%H:%M:%S') <= datetime.strptime(x.get("Event End Date"), "%H:%M:%S"))):
                        return True
                return False
        a.close()


#the below needs to include a list to easily block the dates in the JSON
    @classmethod #blocks(schedules) a date with the date and type passed in (type meaning a classifier denoting holiday, school event, etc.)
    def blockDate(cls, event):
        with open("Community_Planner/event_dates.json", "r+") as a:
            existing_data = json.load(a)
            existing_data.append(event)
            a.seek(0)
            json.dump(existing_data, a)
        a.close()

    @classmethod  #unblock a date passed in (i.e remove it from the event_dates.json file which stores all the dates that are "scheduled")
    def unblockDate(cls, dateToUnblock):
        with open("event_dates.json", "r+") as a:
            data = json.load(a)
            for i, x in enumerate(data):
                if datetime.date(datetime.strptime(x.get("Event Date"), '%Y-%m-%d %H:%M:%S')) == datetime.date(datetime.strptime(dateToUnblock,  '%Y-%m-%d')):
                    a.pop(data[i])
            json.dump(data, a)