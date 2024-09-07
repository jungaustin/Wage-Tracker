from datetime import datetime

class Job:
    def __init__(self, title, wage) -> None:
        self.title = title
        self.wage = wage
        self.hours_worked = []
    def add(self, startTime : datetime, endTime : datetime) -> bool:
        if startTime and endTime:
            if startTime < endTime:
                self.hours_worked.append([startTime, endTime])
                return True
            else:
                return False
    def addToSheet(self, startTime : datetime, endTime : datetime, sh, date_format):
        startTime = startTime.replace(second=0, microsecond=0)
        endTime = endTime.replace(second=0, microsecond=0)
        sheet = sh.worksheet(self.title)
        data = sheet.get_all_values()
        i = 4
        for i, row in enumerate(data[3:], start=4):
            temp = row[0]
            if datetime.strptime(temp, date_format) > startTime:
                break
        startTimeString = startTime.strftime(date_format)
        endTimeString = endTime.strftime(date_format)
        duration = (endTime-startTime).total_seconds()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        sheet.insert_row([startTimeString, endTimeString, f"{hours}:{minutes:02d}"], index = i)
    def changeWage(self, newWage) -> bool:
        self.wage = newWage
        return True