import streamlit as st
from datetime import datetime
from job import Job

st.title("Wage Tracker")

if "jobs" not in st.session_state:
    st.session_state.jobs = []

def input_hours_for_job(job):
    col1, col2, col3 = st.columns(3)
    with col1:
        choose_date = st.date_input("What day did you work?", value=None)
    with col2:
        clock_in = st.time_input(f"Enter clock in time for {job.title}", value=None)
    with col3:
        clock_out = st.time_input(f"Enter clock out time for {job.title}", value=None)
    # clock_in = st.time_input(f"Enter clock in time for {job.title}", value=None)
    # clock_out = st.time_input(f"Enter clock out time for {job.title}", value=None)
    st.write(job.add(clock_in, clock_out))

def create_new__job():
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
        if wage_input:
            for job in st.session_state.jobs:
                if job.title == job_title_input:
                    job.changeWage(wage_input)


action = st.radio("What would you like to do?", ("Create a new job", "Add hours to an existing job", "Clock In/Out"))

if action == "Create a new job":
    create_new__job()

elif action == "Add hours to an existing job":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)

    selected_job = next((job for job in st.session_state.jobs if job.title == selected_job_title), None)
    if selected_job:
        input_hours_for_job(selected_job)

elif action == "Clock In/Out":
    job_titles = [job.title for job in st.session_state.jobs]
    selected_job_title = st.selectbox("Select Job", job_titles)
    st.button("Clock In")

if st.session_state.jobs:
    st.columns(len(st.session_state.jobs))
    st.write("### Job List")
    for job in st.session_state.jobs:
        st.write(f"**{job.title}**: ${job.wage:.2f}/hr, Total Hours: {getattr(job, 'hours', 0):.2f}")
