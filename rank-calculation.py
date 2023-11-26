import pandas as pd
import os

# Assuming your data is in a DataFrame named 'df'
# Replace this with your actual data or load it from a file
df = pd.read_csv(r'D:\Me\concordia\Notes\SE4AI\project\Implementation\Implementation-Git\SOEN-691-Project\Clustering-data.csv')

# Define weights
weights = {'Commits Between Start End': 0.2,
           'Complexity Involved': 0.4,
           'Lines of code changed': 0.4,
           }

# Weighted Average
df['Weighted Average'] = (df[list(weights.keys())] * pd.Series(weights)).sum(axis=1) / sum(weights.values())

# Weighted Geometric Mean
df['Weighted Geometric Mean'] = (df[list(weights.keys())] ** pd.Series(weights)).prod(axis=1) ** (1 / sum(weights.values()))

# Sort by the selected methods in descending order
df_sorted_average = df.sort_values(by='Weighted Average', ascending=False)
df_sorted_geometric_mean = df.sort_values(by='Weighted Geometric Mean', ascending=False)

# Display the top 3 ML SATD types for each method
top3_average = df_sorted_average[['ML Pipeline Stage', 'ML TD Type', 'Weighted Average']].head(3)
top3_geometric_mean = df_sorted_geometric_mean[['ML Pipeline Stage', 'ML TD Type', 'Weighted Geometric Mean']].head(3)


print(top3_average)
print(top3_geometric_mean)
# # Output file path
# output_file_path = r'D:\Me\concordia\Notes\SE4AI\project\Implementation\Implementation-Git\SOEN-691-Project\ML_SATD_Rankings_v3.csv'

# # Check if the output file exists
# file_exists = os.path.isfile(output_file_path)

# # Append the results to a CSV file with headers
# top3_average.to_csv(output_file_path, mode='a', header=not file_exists, index=False)
# top3_geometric_mean.to_csv(output_file_path, mode='a', header=not file_exists, index=False)

# print(f"Results appended to {output_file_path}")
