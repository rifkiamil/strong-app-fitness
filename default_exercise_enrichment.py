from google.cloud import bigquery
import pandas as pd
import openai
import json

from datetime import datetime, timezone

# Set Google Cloud project ID
project_id = "rifkiamil-strong-00-dev"

# Set Google Cloud JSON key file
key_file = "keyfile/keyfile.json"

# Set OpenAI API key
with open("keyfile/chatgpt.json", "r") as file:
    data = json.load(file)
    openai.api_key = data["private_key_id"]

# Set the BigQuery dataset and table you want to query
dataset_id = "raw"
table_id = "default_exercise"

# Initialize the BigQuery client
client = bigquery.Client.from_service_account_json(key_file, project=project_id)

sql = f"""SELECT
  default_exercise_id,
  default_app_id,
  default_app_version,
  exercise_name
FROM
  `rifkiamil-strong-00-dev.raw.default_exercise`
"""

query_job = client.query(sql)
result = query_job.result()

# Convert the result to a pandas dataframe using to_dataframe()
df = result.to_dataframe()


def build_prompt(exercise_names):
    prompt = "Categorize the following exercises as either upper body or lower body:\n\n"
    for name in exercise_names:
        prompt += f"{name}: "
    prompt += "\n\n"
    return prompt


def call_gpt_api(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()

    # Parse the answer to map back to the exercise names
    answers = answer.split("\n")
    exercise_categories = {}

    for ans in answers:
        exercise, category = ans.split(":")
        exercise = exercise.strip()
        category = category.strip()
        exercise_categories[exercise] = category

    return exercise_categories


prompt = build_prompt(df['exercise_name'].tolist())
exercise_categories = call_gpt_api(prompt)

categories_df = pd.DataFrame(list(exercise_categories.items()), columns=['exercise_name', 'exercise_category'])
merged_df = df.merge(categories_df, on='exercise_name')
merged_df.to_csv("exercise_categories.csv", index=False)

print(merged_df)
