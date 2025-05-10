import pandas as pd

# Replace 'your_file.csv' with the actual path to your Starbucks CSV
df = pd.read_csv('/Users/williamcook/ist356M001SP25/project-williscook/Cache/Chick-Fil-A-Nutrition-Fact.csv')

# Display the column names
print(list(df.columns))