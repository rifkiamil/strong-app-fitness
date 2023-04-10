from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timezone


# Set your Google Cloud project ID
project_id = "rifkiamil-strong-00-dev"

# Set your Google Cloud JSON key file
key_file = "keyfile/keyfile.json"

# Set the BigQuery dataset and table you want to query
dataset_id = "raw"
table_id = "strong_all_users"

# Initialize the BigQuery client
client = bigquery.Client.from_service_account_json(key_file, project=project_id)

# Define the SQL query
sql = f"""
SELECT
  *
FROM
  `rifkiamil-strong-00-dev.raw.strong_all_users` AS u
LEFT OUTER JOIN
  `rifkiamil-strong-00-dev.raw.execrise_type` AS e
ON
  u.Exercise_Name = e.exercise
WHERE
  batch_id = 21
"""

pd.set_option("display.max_columns", 20)
# Create dataframe using BigQuery to_dataframe()
df = client.query(sql).to_dataframe()

print(df.head(10))
print(df.dtypes)

# convert the 'Date' column to a string
df['Date_str'] = df['Date'].dt.strftime('%Y-%m-%d')

# concatenate the 'Date_str' and 'Workout_Name' columns to create a unique key
df['Key'] = df['Date_str'].str.cat(df['Workout_Name'], sep='_')

# count the number of unique occurrences of each key in the dataframe
unique_count = df['Key'].nunique()

# find the oldest and newest date in the dataframe
oldest_date = df['Date'].min()
newest_date = df['Date'].max()

# calculate the length of time in days between the oldest and newest date
time_diff_days = (newest_date - oldest_date).days

# Reps between Upper body and Lower body
lower_reps = df[df["upper_Lower_body"]=="Lower"]["Reps"].astype(int).sum()
upper_reps = df[df["upper_Lower_body"]=="Upper"]["Reps"].astype(int).sum()
total_reps = lower_reps + upper_reps
ratio = round(upper_reps / lower_reps, 2)

print("\n\n")
# print the results
print("Oldest date:", oldest_date)
print("Newest date:", newest_date)
print("Time difference in days:", time_diff_days)
print("You worked out:", unique_count)
print("Total reps", upper_reps)
print("Total reps for Lower body exercises:", lower_reps)
print("Total reps for Upper body exercises:", upper_reps)
print(f"For every 1 lower body workout you do {ratio} upper body workouts.")

print("\n")
# Lower Body Work Out
lower_body_df = df[df["upper_Lower_body"] == "Lower"]
if len(lower_body_df) > 0:
    last_time = pd.to_datetime(lower_body_df["Date"].max())
    days_since_last_time = (datetime.now(timezone.utc) - last_time).days
    exercise_name = lower_body_df.iloc[-1]["Exercise_Name"]
    print("Last time Lower body exercise was done:", last_time)
    print("Days since last Lower body exercise:", days_since_last_time)
    print("Last Lower body exercise performed:", exercise_name)
else:
    print("No Lower body exercises found in DataFrame.")

print("\n\n")

# Top 3 and Bottom 3 Lower Body Work Out
lower_body_df = df[df["upper_Lower_body"] == "Lower"]
if len(lower_body_df) > 0:
    # Group by Workout_Name and sum the Reps for each group
    workout_counts = lower_body_df.groupby("Exercise_Name")["Reps"].sum()
    # Sort by the Reps column and get the top and bottom 3
    top_3_workouts = workout_counts.nlargest(3)
    bottom_3_workouts = workout_counts.nsmallest(3)
    # Print the results
    print("Top 3 Lower Body Workout by Reps:")
    print(top_3_workouts.to_string())
    print("\n\n")

    print("Bottom 3 Lower Body Workout by Reps:")
    print(bottom_3_workouts.to_string())
else:
    print("No Lower body exercises found in DataFrame.")