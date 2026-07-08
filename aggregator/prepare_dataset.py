import os
import pandas as pd
from sklearn.model_selection import train_test_split

# -----------------------------------
# Load Dataset
# -----------------------------------

dataset_path = "../datasets/framingham.csv"

df = pd.read_csv(dataset_path)

print("Original Dataset Shape:", df.shape)

# -----------------------------------
# Remove duplicate rows
# -----------------------------------

df = df.drop_duplicates()

# -----------------------------------
# Fill missing values
# -----------------------------------

df = df.fillna(df.median(numeric_only=True))

print("After Cleaning:", df.shape)

# -----------------------------------
# Shuffle dataset
# -----------------------------------

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# -----------------------------------
# Train/Test Split
# -----------------------------------

train_df, test_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["TenYearCHD"]
)

# -----------------------------------
# Split Training Data into 3 Parts
# -----------------------------------

worker1, temp = train_test_split(
    train_df,
    test_size=2/3,
    random_state=42,
    stratify=train_df["TenYearCHD"]
)

worker2, worker3 = train_test_split(
    temp,
    test_size=0.5,
    random_state=42,
    stratify=temp["TenYearCHD"]
)

# -----------------------------------
# Create Output Folder
# -----------------------------------

output_folder = "../datasets/processed"

os.makedirs(output_folder, exist_ok=True)

# -----------------------------------
# Save CSV Files
# -----------------------------------

worker1.to_csv(f"{output_folder}/worker1.csv", index=False)
worker2.to_csv(f"{output_folder}/worker2.csv", index=False)
worker3.to_csv(f"{output_folder}/worker3.csv", index=False)

test_df.to_csv(f"{output_folder}/test.csv", index=False)

print("\nDataset Prepared Successfully!\n")

print("Worker 1:", len(worker1))
print("Worker 2:", len(worker2))
print("Worker 3:", len(worker3))
print("Test Set:", len(test_df))
