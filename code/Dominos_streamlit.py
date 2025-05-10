import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("🍕 Pizza Nutrition App")

#Display current working directory for debugging
st.caption("📁 Current working directory:")
st.code(os.getcwd())

#Sample DataFrame for nutrient display
st.header("Pizza Nutrition Facts (per slice)")
Pizza_data = {
    "Pizza": ["Cheese", "Pepperoni", "Veggie", "Meat Lovers"],
    "Calories (cal)": [270, 310, 250, 330],
    "Carbohydrates (g)": [33, 34, 30, 35],
    "Sugar (g)": [3, 2, 4, 3],
    "Protein (g)": [12, 14, 11, 16]
}
Dominos_df = pd.DataFrame(Pizza_data)

# Filtering Controls
st.subheader("🔍 Filter Options")

# Thresholds
protein_threshold = Dominos_df["Protein (g)"].median()
sugar_threshold = Dominos_df["Sugar (g)"].median()
carb_threshold = Dominos_df["Carbohydrates (g)"].median()

# Filter selections
protein_filter = st.selectbox("Protein Filter", ["All", "High Protein", "Low Protein"])
sugar_filter = st.selectbox("Sugar Filter", ["All", "High Sugar", "Low Sugar"])
carb_filter = st.selectbox("Carbohydrates Filter", ["All", "High Carbs", "Low Carbs"])

# Apply filters
filtered_Dominos = Dominos_df.copy()

if protein_filter == "High Protein":
    filtered_Dominos = filtered_Dominos[filtered_Dominos["Protein (g)"] > protein_threshold]
elif protein_filter == "Low Protein":
    filtered_Dominos = filtered_Dominos[filtered_Dominos["Protein (g)"] <= protein_threshold]

if sugar_filter == "High Sugar":
    filtered_Dominos = filtered_Dominos[filtered_Dominos["Sugar (g)"] > sugar_threshold]
elif sugar_filter == "Low Sugar":
    filtered_Dominos = filtered_Dominos[filtered_Dominos["Sugar (g)"] <= sugar_threshold]

if carb_filter == "High Carbs":
    filtered_Dominos = filtered_Dominos[filtered_Dominos["Carbohydrates (g)"] > carb_threshold]
elif carb_filter == "Low Carbs":
    filtered_Dominos = filtered_Dominos[filtered_Dominos["Carbohydrates (g)"] <= carb_threshold]

st.dataframe(filtered_Dominos)

# Load and display Markdown content
st.header("📄 Nutrition Info Summary (Markdown)")

md_path = "pizza_nutrition.md"  # Adjust this if your file is in a different location

try:
    with open(md_path, "r") as file:
        md_content = file.read()
    st.markdown(md_content, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Markdown file not found at: `{md_path}`. Please check the file path.")
