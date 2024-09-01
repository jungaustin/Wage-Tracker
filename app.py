import streamlit as st
from datetime import datetime
from job import Job
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# How to authorize google sheets access
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
client = gspread.authorize(creds)

# Standard Date Format
date_format = "%m/%d/%Y %H:%M:%S"
sh = client.open("Wages for Streamlit Project")



if "jobs" not in st.session_state:
    st.session_state.jobs = []

    # Next part is to get all the data already in the spreadsheet
    worksheets = sh.worksheets()
    for worksheet in worksheets:
        data = worksheet.get_all_values()
        if len(data) != 0:
            temp = Job(data[0][1], float(data[1][1]))
            for row in data[3:]:
                start = datetime.strptime(row[0], date_format)
                end = datetime.strptime(row[1], date_format)
                temp.add(start, end)
            if not any(job.title == temp.title for job in st.session_state.jobs):
                st.session_state.jobs.append(temp)

st.title("Wage Tracker")

if "add_button" not in st.session_state:
    st.session_state.add_button = False

action = st.radio("What would you like to do?", ("Create a new job", "Add hours to an existing job", "Remove hours from existing job", "Clock In/Out"))

if action == "Create a new job":
    job_title_input = st.text_input(
        "Job Title Input",
        label_visibility="collapsed",
        disabled=False,
        placeholder="New Job Title",
    )

    if job_title_input:
        wage_input = st.number_input("Enter Hourly Wage", min_value=0.0, format="%.2f", label_visibility="visible", disabled=False, placeholder="Enter Wage Amount")
        found = False
        for job in st.session_state.jobs:
            if job.title == job_title_input:
                found = True
        if not found:
            st.session_state.jobs.append(Job(job_title_input, 0))
            sheet = sh.add_worksheet(job_title_input, 0, 0)
            sheet.update_acell('A1', "Job")
            sheet.update_acell('B1', job_title_input)
            sheet.update_acell('A2', "Wage")
            sheet.update_acell('A3', "Start")
            sheet.update_acell('B3', "End")
            sheet.update_acell('C3', "Total")
        if wage_input:
            for job in st.session_state.jobs:
                if job.title == job_title_input:
                    job.changeWage(wage_input)
                    sheet = sh.worksheet(job_title_input)
                    sheet.update_acell('B2', wage_input)

elif action == "Add hours to an existing job":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)

    selected_job = next((job for job in st.session_state.jobs if job.title == selected_job_title), None)
    if selected_job:
        col1, col2, col3 = st.columns(3)
        with col1:
            choose_date = st.date_input("What day did you work?", value=None)
        with col2:
            clock_in = st.time_input(f"Enter clock in time for {selected_job.title}", value=None)
        with col3:
            clock_out = st.time_input(f"Enter clock out time for {selected_job.title}", value=None)
        add_hours = st.button("Add")
        if add_hours:
            st.session_state.add_button = True
        if st.session_state.add_button:
            start_time = datetime.combine(choose_date, clock_in)
            end_time = datetime.combine(choose_date, clock_out)
            st.write(selected_job.add(start_time, end_time))
            selected_job.addToSheet(start_time, end_time, sh, date_format)
            st.session_state.add_button = False

## elif action == "Remove hours from existing job":
    

elif action == "Clock In/Out":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)
    selected_job = next((job for job in st.session_state.jobs if job.title == selected_job_title), None)
    if selected_job:
        col1, col2 = st.columns(2)
        with col1:
            clock_in = st.button("Clock In")
            clock_in_time = datetime.now()
        with col2:
            clock_out = st.button("Clock Out")
            clock_out_time = datetime.now()
        if clock_in:
            curr_time = datetime.now()
            st.write("Clock in time: " + clock_in_time.strftime("%m-%d-%Y %H:%M"))
        if clock_out:
            curr_time = datetime.now()
            st.write("Clock out time: " + clock_out_time.strftime("%m-%d-%Y %H:%M"))
            if clock_in_time:
                selected_job.add(clock_in_time, clock_out_time)

if st.session_state.jobs:
    st.write("## Job List")
    columns = st.columns(len(st.session_state.jobs))
    for i, job in enumerate(st.session_state.jobs):
        with columns[i]:
            st.write("#### " + f"**{job.title}**: \n #### **${job.wage:.2f}/hr, Total Hours: {getattr(job, 'hours', 0):.2f}** \n")
            for hours_worked in job.hours_worked[-6:]:
                st.write("##### " + "Date: " + hours_worked[0].strftime("%m-%d-%Y"))
                st.write("##### " + hours_worked[0].strftime("%H:%M") + " - " + hours_worked[1].strftime("%H:%M"))
