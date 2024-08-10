from datetime import datetime

# Define two datetime objects
time1 = datetime(2024, 8, 7, 12, 0, 0)  # Year, Month, Day, Hour, Minute, Second
time2 = datetime(2024, 8, 7, 15, 30, 0)  # Year, Month, Day, Hour, Minute, Second

# Calculate the difference
time_difference = time2 - time1

# Display the difference
print("Time Difference:", time_difference)
print("Total seconds:", time_difference.total_seconds())