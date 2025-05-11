import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load McDonald's data
McDonald_df = pd.read_csv('/Users/williamcook/ist356M001SP25/project-williscook/Cache/McDonald.csv')

# Clean column names
McDonald_df.columns = McDonald_df.columns.str.strip()

# Rename columns for clarity
McDonald_df.rename(columns={
    'Calories': 'Calories',
    'Protein': 'Protein (g)',
    'Sugars': 'Sugar (g)',
    'Carbohydrates': 'Carbohydrates (g)'
}, inplace=True)

# Drop rows with missing values
McDonald_df = McDonald_df[['Item', 'Protein (g)', 'Sugar (g)', 'Carbohydrates (g)', 'Calories']].dropna()

# Ensure numeric types
McDonald_df['Protein (g)'] = pd.to_numeric(McDonald_df['Protein (g)'], errors='coerce')
McDonald_df['Sugar (g)'] = pd.to_numeric(McDonald_df['Sugar (g)'], errors='coerce')

# Streamlit config
st.set_page_config(page_title="🍔 McDonald's Nutrition Filter", layout="wide")
st.title("🍔 McDonald's Nutrition Filter")
st.subheader("Find items with High Protein and Low Sugar")

# Sliders for filtering
protein_min, protein_max = st.slider(
    "Protein range (g):",
    float(McDonald_df['Protein (g)'].min()),
    float(McDonald_df['Protein (g)'].max()),
    (15.0, float(McDonald_df['Protein (g)'].max()))
)

sugar_min, sugar_max = st.slider(
    "Sugar range (g):",
    float(McDonald_df['Sugar (g)'].min()),
    float(McDonald_df['Sugar (g)'].max()),
    (0.0, 20.0)
)

# Filter data
filtered_McDonald = McDonald_df[
    (McDonald_df['Protein (g)'] >= protein_min) & (McDonald_df['Protein (g)'] <= protein_max) &
    (McDonald_df['Sugar (g)'] >= sugar_min) & (McDonald_df['Sugar (g)'] <= sugar_max)
]

# Search bar
search_term = st.text_input("🔍 Search by item name:")
if search_term:
    filtered_McDonald = filtered_McDonald[filtered_McDonald['Item'].str.contains(search_term, case=False, na=False)]

# Show results
st.write(f"🍟 Found {len(filtered_McDonald)} McDonald's items matching your filters:")
st.dataframe(filtered_McDonald.reset_index(drop=True))

# Plot results
st.subheader("Top Filtered McDonald's Items by Protein")
top_items = filtered_McDonald.sort_values(by='Protein (g)', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_items, x='Protein (g)', y='Item', palette='flare', ax=ax)
ax.set_title("Top High Protein, Low Sugar McDonald's Items")
st.pyplot(fig)
