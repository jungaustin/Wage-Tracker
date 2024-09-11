import streamlit as st
from datetime import datetime
from job import Job
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


# Authorize Google Sheets access
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
client = gspread.authorize(creds)
sh = client.open("Wages for Streamlit Project")
date_format = "%m/%d/%Y %H:%M:%S"

def find_job_by_title(title):
    return next((job for job in st.session_state.jobs if job.title == title), None)


@st.cache_data
def load_jobs():
    worksheets = sh.worksheets()
    jobs = []
    for worksheet in worksheets:
        data = worksheet.get_all_values()
        if len(data) != 0:
            temp = Job(data[0][1], float(data[1][1]))
            for row in data[3:]:
                start = datetime.strptime(row[0], date_format)
                end = datetime.strptime(row[1], date_format)
                temp.add(start, end)
            if not any(job.title == temp.title for job in jobs):
                jobs.append(temp)
    return jobs

if "jobs" not in st.session_state:
    st.session_state.jobs = load_jobs()
    
if "clock_in_time" not in st.session_state:
    st.session_state.clock_in_time = None

st.title("Wage Tracker")

action = st.radio("What would you like to do?", ("Create a new job", "Add hours to an existing job", "Remove hours from existing job", "Clock In/Out", "Get Wage Total"))

if action == "Create a new job":
    with st.form(key='create_job_form'):
        job_title_input = st.text_input("Job Title Input", placeholder="New Job Title")
        wage_input = st.number_input("Enter Hourly Wage", min_value=0.0, format="%.2f", placeholder="Enter Wage Amount")
        submit_button = st.form_submit_button("Create Job")
        if submit_button and job_title_input:
            if job_title_input not in [job.title for job in st.session_state.jobs]:
                st.session_state.jobs.append(Job(job_title_input, wage_input))
                sheet = sh.add_worksheet(job_title_input, 0, 0)
                sheet.update_acell('A1', "Job")
                sheet.update_acell('B1', job_title_input)
                sheet.update_acell('A2', "Wage")
                sheet.update_acell('A3', "Start")
                sheet.update_acell('B3', "End")
                sheet.update_acell('C3', "Total")
                sheet.update_acell('B2', wage_input)

elif action == "Add hours to an existing job":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)
    selected_job = find_job_by_title(selected_job_title)
    
    with st.form(key='add_hours_form'):
        choose_date = st.date_input("What day did you work?")
        clock_in = st.time_input(f"Enter clock in time for {selected_job.title}")
        clock_out = st.time_input(f"Enter clock out time for {selected_job.title}")
        add_hours = st.form_submit_button("Add")
        if add_hours and clock_in and clock_out:
            start_time = datetime.combine(choose_date, clock_in)
            end_time = datetime.combine(choose_date, clock_out)
            st.write(selected_job.add(start_time, end_time))
            selected_job.addToSheet(start_time, end_time, sh, date_format)

elif action == "Remove hours from existing job":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)
    selected_job = find_job_by_title(selected_job_title)
    
    with st.form(key="remove_hours_form"):
        start_times = [datetime.strftime(time[0], date_format) for time in selected_job.hours_worked]
        selected_removal = st.selectbox("What do you want to remove", start_times)
        remove_hours = st.form_submit_button("Remove")
        if remove_hours and selected_removal:
            datetime_remove = datetime.strptime(selected_removal, date_format)
            st.write(selected_job.removeFromSheet(sh, datetime_remove, date_format))
            action = "Remove hours from existing job"

elif action == "Clock In/Out":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)
    selected_job = find_job_by_title(selected_job_title)
    if selected_job:
        col1, col2 = st.columns(2)
        with col1:
            clock_in = st.button("Clock In")
            if clock_in:
                st.session_state.clock_in_time = datetime.now()
                st.write("Clock in time: " + st.session_state.clock_in_time.strftime("%m-%d-%Y %H:%M"))
        with col2:
            clock_out = st.button("Clock Out")
            if clock_out:
                if st.session_state.clock_in_time:
                    clock_out_time = datetime.now()
                    st.write("Clock out time: " + clock_out_time.strftime("%m-%d-%Y %H:%M"))
                    selected_job.add(st.session_state.clock_in_time, clock_out_time)
                    selected_job.addToSheet(st.session_state.clock_in_time, clock_out_time, sh, date_format)
                    st.write(True)
                    st.session_state.clock_in_time = None
elif action == "Get Wage Total":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)
    selected_job = find_job_by_title(selected_job_title)
    if selected_job:
        
        with st.form(key="Get Wage Total"):
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            get_wages = st.form_submit_button("Get Wages")
            if get_wages and start_date <= end_date:
                selected_job.getTotal(sh, datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.max.time()), date_format)