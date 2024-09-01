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
        sheet = sh.worksheet(self.title)
        startTimeString = startTime.strftime(date_format)
        endTimeString = endTime.strftime(date_format)
        duration = (endTime-startTime).total_seconds()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        sheet.append_row([startTimeString, endTimeString, f"{hours}:{minutes:02d}"])
    def changeWage(self, newWage) -> bool:
        self.wage = newWage
        return True