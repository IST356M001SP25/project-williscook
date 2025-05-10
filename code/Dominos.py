import pdfplumber
import pandas as pd

def fix_reverse(text):
    """Fix reversed strings from PDF parsing."""
    if isinstance(text, str):
        return text[::-1].strip()
    return text

# Define possible clean column headers
base_columns = [
    "Item Name",
    "Serving Size",
    "Weight (g)",
    "Calories",
    "Calories from Fat",
    "Total Fat (g)",
    "Saturated Fat (g)",
    "Trans Fat (g)",
    "Cholesterol (mg)",
    "Sodium (mg)",
    "Carbohydrates (g)",
    "Fiber (g)",
    "Sugars (g)",
    "Protein (g)"
]

# Open the Domino's PDF
with pdfplumber.open("DominosNutritionGuide.pdf") as pdf:
    all_tables = []

    for page_num, page in enumerate(pdf.pages, start=1):
        print(f"Processing page {page_num}...")

        tables = page.extract_tables()
        for table in tables:
            if not table or len(table) < 2:
                continue

            pizza_df = pd.DataFrame(table)

            pizza_df = df.dropna(axis=1, how='all')

            if pizza_df.shape[0] < 2:
                continue

            # Remove header rows repeated in body
            if any("Calories" in str(cell) for cell in pizza_df.iloc[0]):
                pizza_df = pizza_df[1:]

            pizz_df = pizza_df.applymap(fix_reverse)

            all_tables.append(pizza_df)

# Combine and clean
if all_tables:
    combined_pizza__df = pd.concat(all_tables, ignore_index=True)

    # Trim or pad column headers to fit the actual column count
    col_count = combined_pizza__df.shape[1]
    if col_count <= len(base_columns):
        columns = base_columns[:col_count]
    else:
        columns = base_columns + [f"Extra_{i}" for i in range(col_count - len(base_columns))]

    combined_pizza__df = columns

    # Save to CSV
    combined_pizza__df.to_csv("DominosNutrition_Cleaned.csv", index=False)
    print("✅ Saved cleaned nutrition data to 'DominosNutrition_Cleaned.csv'")
else:
    print("⚠️ No tables extracted from the PDF.")
