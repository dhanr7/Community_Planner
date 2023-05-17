#Class to manage events/manage schedules
#Yet to be written, tested, and implemented
#Stores all dates that have been taken/ scheduled with their metadata (event_dates.txt)

import datetime
from datetime import datetime
import os

class ScheduleManager:
    list_holiday_dates_23_24 = [
        "07/04/2023", #American Independence Day
        "08/08/2023", #Mandatory Staff Development Day
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
    ]

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



