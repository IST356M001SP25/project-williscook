import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load Chick-fil-A data
ChickfilA_df = pd.read_csv('/Users/williamcook/Documents/Chick-Fil-A-Nutrition-Fact_latest/Sheet 1-Chick-Fil-A-Nutrition-Fact.csv')

# Clean column names
ChickfilA_df.columns = ChickfilA_df.columns.str.strip()

# Rename for clarity
ChickfilA_df.rename(columns={
    'Breakfast Menu List': 'Item',
    'Protein (G)': 'Protein',
    'Sugar (G)': 'Sugar',
    'Carbohydrates (G)': 'Carbohydrates'
}, inplace=True)

# Drop missing
ChickfilA_df = ChickfilA_df[['Item', 'Protein', 'Sugar', 'Carbohydrates', 'Calories']].dropna()

# Convert to numeric
ChickfilA_df['Protein'] = pd.to_numeric(ChickfilA_df['Protein'], errors='coerce')
ChickfilA_df['Sugar'] = pd.to_numeric(ChickfilA_df['Sugar'], errors='coerce')

# Create single Sweetness Label column
def sugar_label(sugar):
    if sugar > 20:
        return '🍩 High Sugar (Sweet Treat)'
    elif sugar > 10:
        return '⚠️ Moderate Sugar'
    else:
        return '✅ Low Sugar'

ChickfilA_df['Sweet Label'] = ChickfilA_df['Sugar'].apply(sugar_label)

# Streamlit UI
st.title("🐔 Chick-fil-A Nutrition Filter")
st.subheader("Find items with High Protein and Low Sugar")

# Search bar
search_term = st.text_input("🔍 Search by item name:")
if search_term:
    ChickfilA_df = ChickfilA_df[ChickfilA_df['Item'].str.contains(search_term, case=False, na=False)]

# Sliders
protein_min, protein_max = st.slider(
    "Protein range (grams):",
    float(ChickfilA_df['Protein'].min()),
    float(ChickfilA_df['Protein'].max()),
    (15.0, float(ChickfilA_df['Protein'].max()))
)

sugar_min, sugar_max = st.slider(
    "Sugar range (grams):",
    float(ChickfilA_df['Sugar'].min()),
    float(ChickfilA_df['Sugar'].max()),
    (0.0, 10.0)
)

# Filter data
filtered_ChickfilA = ChickfilA_df[
    (ChickfilA_df['Protein'] >= protein_min) & (ChickfilA_df['Protein'] <= protein_max) &
    (ChickfilA_df['Sugar'] >= sugar_min) & (ChickfilA_df['Sugar'] <= sugar_max)
]

# Display result
st.write(f"🍽️ Found {len(filtered_ChickfilA)} items matching your filters:")
st.dataframe(filtered_ChickfilA[['Item', 'Protein', 'Sugar', 'Carbohydrates', 'Calories', 'Sweet Label']].reset_index(drop=True))

# Plot
st.subheader("Top Filtered Items by Protein")
top_items = filtered_ChickfilA.sort_values(by='Protein', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_items, x='Protein', y='Item', palette='flare', ax=ax)
ax.set_title("Top High Protein, Low Sugar Items")
st.pyplot(fig)
