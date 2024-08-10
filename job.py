from datetime import datetime
class Job:
    def __init__(self, title, wage) -> None:
        self.title = title
        self.wage = wage
        self.hours_worked = []
    def add(self, startTime : datetime, endTime : datetime) -> bool:
        self.hours_worked.append([startTime, endTime])