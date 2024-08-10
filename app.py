import streamlit as st
from job import Job

st.title("Wage Tracker")


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

if "jobs" not in st.session_state:
    st.session_state.jobs = []

job_title_input = st.text_input(
    "Job Title Input",
    label_visibility="collapsed",
    disabled=False,
    placeholder="New Job Title",
)

if job_title_input:
    wage_input = st.number_input("Enter Hourly Wage",min_value=0.0, format="%.2f", label_visibility="visible", disabled=False, placeholder="Enter Wage Amount")
    if wage_input:
        temp = Job(job_title_input, wage_input)
        st.session_state.jobs.append(temp)

if st.session_state.jobs:
    st.write("### Job List")
    for job in st.session_state.jobs:
        st.write(f"**{job.title}**: ${job.wage:.2f}/hr")