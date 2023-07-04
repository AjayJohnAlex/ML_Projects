# Installing libraries
# Install the ChEMBL web service package so that we can retrieve bioactivity data from the ChEMBL Database.

# ! pip install chembl_webresource_client
# Importing libraries

# Import necessary libraries
import pandas as pd
from chembl_webresource_client.new_client import new_client

# Search for Target protein
# Target search for Acetylcholinesterase

# Target search for coronavirus
target = new_client.target
target_query = target.search("acetylcholinesterase")
targets = pd.DataFrame.from_dict(target_query)
targets


# Select and retrieve bioactivity data for Human Acetylcholinesterase (first entry)
# We will assign the fifth entry (which corresponds to the target protein, Human Acetylcholinesterase) to the *selected_target* variable


selected_target = targets.target_chembl_id[0]
selected_target

activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")


df = pd.DataFrame.from_dict(res)
df.head()

folder_path = """D:\\Machine_Learning\\ML_Projects\\Drug Discovery\\data\\raw\\"""
df.to_csv(
    f"{folder_path}" + "acetylcholinesterase_01_bioactivity_data_raw.csv", index=False
)
