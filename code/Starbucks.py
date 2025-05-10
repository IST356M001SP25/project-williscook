import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

#Load Data
Starbucks_df = pd.read_csv('/Users/williamcook/ist356M001SP25/project-williscook/Cache/Starbucks.csv')

# Clean column names
Starbucks_df.columns = Starbucks_df.columns.str.strip()


# Drop rows with missing values
Starbucks_df = Starbucks_df[
    ['Item Name', 'Serving Size (g)', 'Energy (Kcal)', 'Fat (g)', 'Carbohydrates (g)', 'Sugar (g)', 'Protein (g)']
].dropna()

# Ensure numeric types
Starbucks_df['Protein (g)'] = pd.to_numeric(Starbucks_df['Protein (g)'], errors='coerce')
Starbucks_df['Sugar (g)'] = pd.to_numeric(Starbucks_df['Sugar (g)'], errors='coerce')

# Streamlit config
st.set_page_config(page_title="Starbucks's Nutrition Filter", layout="wide")
st.title("Starbucks Nutrition Filter")
st.subheader("Find items with High Protein and Low Sugar")

# Sliders for filtering
protein_min, protein_max = st.slider(
    "Protein range (g):",
    float(Starbucks_df['Protein (g)'].min()),
    float(Starbucks_df['Protein (g)'].max()),
    (15.0, float(Starbucks_df['Protein (g)'].max()))
)

sugar_min, sugar_max = st.slider(
    "Sugar range (g):",
    float(Starbucks_df['Sugar (g)'].min()),
    float(Starbucks_df['Sugar (g)'].max()),
    (0.0, 20.0)
)

# Filter data
filtered_Starbucks = Starbucks_df[
    (Starbucks_df['Protein (g)'] >= protein_min) & (Starbucks_df['Protein (g)'] <= protein_max) &
    (Starbucks_df['Sugar (g)'] >= sugar_min) & (Starbucks_df['Sugar (g)'] <= sugar_max)
]

# Show results
st.write(f" Found {len(filtered_Starbucks)} Starbucks's items matching your filters:")
st.dataframe(filtered_Starbucks.reset_index(drop=True))

# Plot results
st.subheader("Top Filtered Starbucks's Items by Protein")
top_items = filtered_Starbucks.sort_values(by='Protein (g)', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_items, x='Protein (g)', y='Item Name', palette='flare', ax=ax)
ax.set_title("Top High Protein, Low Sugar Starbucks's Items")
st.pyplot(fig)