import pandas as pd
import os

# Read the original data from Clustering.csv
file_path = r'D:\Me\concordia\Notes\SE4AI\project\Implementation\Implementation-Git\SOEN-691-Project\Clustering-data.csv'
df = pd.read_csv(file_path)

# Define weights
weights = {'Commits Between Start End': 0.2,
           'Complexity Involved': 0.4,
           'Lines of code changed': 0.4,
           }

# Calculate Weighted Average for each row
df['Weighted Average'] = (df[list(weights.keys())] * pd.Series(weights)).sum(axis=1) / sum(weights.values())

# Save the updated DataFrame (including the new column) back to the same CSV file
df.to_csv(file_path, index=False)

print("Weighted Average column appended and CSV updated.")
