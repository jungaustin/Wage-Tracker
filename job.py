from datetime import datetime
from fpdf import FPDF

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
        if startTime >= endTime:
            return False
        sheet = sh.worksheet(self.title)
        data = sheet.get_all_values()
        
        i = 4
        latest = True
        for i, row in enumerate(data[3:], start=4):
            temp = row[0]
            if datetime.strptime(temp, date_format) > startTime:
                latest = False
                break
        if len(data) == 3:
            latest = False
        startTimeString = startTime.strftime(date_format)
        endTimeString = endTime.strftime(date_format)
        duration = (endTime-startTime).total_seconds()
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        i = i if not latest else i+1
        sheet.insert_row([startTimeString, endTimeString, f"{hours}:{minutes:02d}"], index = i)
        return True
    
    def removeFromSheet(self, sh, startTime, date_format):
        sheet = sh.worksheet(self.title)
        data = sheet.get_all_values()
        i = 4
        for i, row in enumerate(data[3:], start=4):
            temp = row[0]
            if datetime.strptime(temp, date_format) == startTime:
                break
        sheet.delete_rows(i)
        for shift in self.hours_worked:
            if shift[0] == startTime:
                self.hours_worked.remove(shift)
                break
        return True
        
    def getTotal(self, sh, startDate, endDate, date_format):
        sheet = sh.worksheet(self.title)
        data = sheet.get_all_values()
        i = 4
        rowStart = None
        rowEnd = None
        for i, row in enumerate(data[3:], start=4):
            temp = row[0]
            if datetime.strptime(temp, date_format) >= startDate:
                rowStart = i
                break
        if rowStart is not None:
            print(rowStart)
            for i, row in enumerate(data[rowStart-1:], start=rowStart):
                temp = row[0]
                if datetime.strptime(temp, date_format) >= endDate:
                    rowEnd = i-1
                    break
            print(rowEnd)
            if rowEnd is None:
                rowEnd = len(data)
            self.generatePDF(data[rowStart-1:rowEnd], int(data[1][1]))
            return True
        return False
    #yoinked and edited from chatgpt for testing
    def generatePDF(self, selected_rows, wage):
        # Create a PDF document
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Set font
        pdf.set_font("Arial", size=12)

        # Add a title
        pdf.cell(200, 10, txt="Selected Rows from Google Sheets", ln=True, align='C')
        pdf.ln(10)  # Line break
        
        # Add table header (you can customize this)
        headers = ["Start", "End", "Total Time"]
        for header in headers:
            pdf.cell(50, 10, txt=header, border=1)
        pdf.ln()  # New line for table
        total_hours = 0
        total_minutes = 0
        # Add rows to the PDF
        for row in selected_rows:
            for index, cell in enumerate(row):
                pdf.cell(50, 10, txt=str(cell), border=1)
                if index == len(row) - 1:
                    hours, minutes = str(cell).split(":")
                    total_hours += int(hours)
                    total_minutes += int(minutes)
            pdf.ln()
        
        pdf.cell(50, 10, txt="", border=1)
        pdf.cell(50, 10, txt="Total", border=1)
        total_hours += total_minutes//60
        total_minutes %= 60
        pdf.cell(50, 10, txt=str(total_hours) + ":" + str(f"{total_minutes:02}"), border=1)
        pdf.ln()
        pdf.cell(50, 10, txt="", border=1)
        pdf.cell(50, 10, txt="Wage", border=1)
        pdf.cell(50, 10, txt=str(wage), border=1)
        pdf.ln()
        pdf.cell(50, 10, txt="", border=1)
        pdf.cell(50, 10, txt="Total Wage", border=1)
        
        total_wage = total_hours * wage + total_minutes/60 * wage
        formatted_wage = f"{total_wage:.2f}"
        pdf.cell(50, 10, txt=str(formatted_wage), border=1)
        
        # Save the PDF to a file
        pdf_output = "output.pdf"
        pdf.output(pdf_output)

    def changeWage(self, newWage) -> bool:
        self.wage = newWage
        return True