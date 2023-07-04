import pandas as pd

file_path = """D:\\Machine_Learning\\ML_Projects\\Drug Discovery\\data\\raw\\"""
file_name = """acetylcholinesterase_01_bioactivity_data_raw.csv"""


df = pd.read_csv(f"{file_path}{file_name}")
df.head()
# df.isna().sum()


df2 = df[df.standard_value.notna()]
df2 = df2[df.canonical_smiles.notna()]
df2.head()

len(df2.canonical_smiles.unique())

df2_nr = df2.drop_duplicates(["canonical_smiles"])
df2_nr

# Data pre-processing of the bioactivity data
# Combine the 3 columns (molecule_chembl_id,canonical_smiles,standard_value) and bioactivity_class into a DataFrame


selection = ["molecule_chembl_id", "canonical_smiles", "standard_value"]
df3 = df2_nr[selection]
df3.head()


df3.to_csv(
    f"D:\\Machine_Learning\\ML_Projects\\Drug Discovery\\data\\processed\\acetylcholinesterase_02_bioactivity_data_preprocessed.csv",
    index=False,
)


# Labeling compounds as either being active, inactive or intermediate
# The bioactivity data is in the IC50 unit. Compounds having values of less than 1000 nM will be considered to be active while those greater than 10,000 nM will be considered to be inactive. As for those values in between 1,000 and 10,000 nM will be referred to as intermediate.

bioactivity_threshold = []
for i in df3.standard_value:
    if float(i) >= 10000:
        bioactivity_threshold.append("inactive")
    elif float(i) <= 1000:
        bioactivity_threshold.append("active")
    else:
        bioactivity_threshold.append("intermediate")

bioactivity_class = pd.Series(bioactivity_threshold, name="class")
df5 = pd.concat([df3, bioactivity_class], axis=1)
df5.head()


df5.to_csv(
    "D:\\Machine_Learning\\ML_Projects\\Drug Discovery\\data\\processed\\acetylcholinesterase_03_bioactivity_data_curated.csv",
    index=False,
)
