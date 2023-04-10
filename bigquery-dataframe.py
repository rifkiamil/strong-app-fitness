from google.cloud import bigquery
import pandas as pd

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
  user_id as user_id,
  COUNT(user_id) as number_of_users
FROM
  `rifkiamil-strong-00-dev.raw.strong_all_users`
GROUP BY
  user_id
"""

# Create dataframe using BigQuery to_dataframe()
df = client.query(sql).to_dataframe()

print(df.head(10))