#!/bin/bash
deactivate_venv() {
    echo "Deactivating virtual environment..."
    deactivate
    exit 0
}
source /Users/austin/Desktop/Home/Projects/"Completed Projects"/"Wage Tracker"/WageTracker/bin/activate
trap deactivate_venv EXIT
streamlit run /Users/austin/Desktop/Home/Projects/"Completed Projects"/"Wage Tracker"/app.py &
# /Users/austin/Desktop/Home/Projects/"Completed Projects"/"Wage Tracker"/WageTracker/bin/streamlit run app.py --browser.serverAddress="localhost" --browser.gatherUsageStats=false

STREAMLIT_PID=$!
sleep 300
kill $STREAMLIT_PID 2>/dev/null
deactivate_venv
