import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from job import Job
from datetime import datetime

creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
client = gspread.authorize(creds)

if "jobs" not in st.session_state:
    st.session_state.jobs = []

sh = client.open("Wages for Streamlit Project")
worksheets = sh.worksheets()
for worksheet in worksheets:
    data = worksheet.get_all_values()
    if len(data) != 0:
        temp = Job(data[0][1], data[1][1])
        date_format = "%m/%d/%Y %H:%M:%S"
        for row in data[3:]:
            start = datetime.strptime(row[0], date_format)
            end = datetime.strptime(row[1], date_format)
            temp.add(start, end)
        st.session_state.jobs.append(temp)
        
for job in st.session_state.jobs:
    st.write(job.title)
    for shifts in job.hours_worked:
        st.write("" + shifts[0].strftime(date_format) + "   " + shifts[1].strftime(date_format))