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
    def changeWage(self, newWage) -> bool:
        self.wage = newWage
        return True
    