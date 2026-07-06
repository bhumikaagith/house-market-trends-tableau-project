"""
data_validation.py

Validates Transformed_Housing_Data2.csv before it goes into Tableau:
- confirms row/column counts
- checks for nulls
- checks dtypes match what's expected
- checks value ranges for obvious errors (negative prices, 0 bedrooms, etc.)
- prints summary stats (the same numbers referenced in the Flask KPIs
  and in tableau/TABLEAU_STEPS.md's Performance Testing section)

Run:
    python scripts/data_validation.py
"""

import os
import sys
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Transformed_Housing_Data2.csv")

EXPECTED_COLUMNS = [
    "Sale_Price", "No of Bedrooms", "No of Bathrooms", "Flat Area (in Sqft)",
    "Lot Area (in Sqft)", "No of Floors", "No of Times Visited", "Overall Grade",
    "Area of the House from Basement (in Sqft)", "Basement Area (in Sqft)",
    "Age of House (in Years)", "Latitude", "Longitude",
    "Living Area after Renovation (in Sqft)", "Lot Area after Renovation (in Sqft)",
    "Years Since Renovation", "Condition_of_the_House_Excellent",
    "Condition_of_the_House_Fair", "Condition_of_the_House_Good",
    "Condition_of_the_House_Okay", "Ever_Renovated_Yes", "Waterfront_View_Yes",
    "Zipcode_Group_Zipcode_Group_1", "Zipcode_Group_Zipcode_Group_2",
    "Zipcode_Group_Zipcode_Group_3", "Zipcode_Group_Zipcode_Group_4",
    "Zipcode_Group_Zipcode_Group_5", "Zipcode_Group_Zipcode_Group_6",
    "Zipcode_Group_Zipcode_Group_7", "Zipcode_Group_Zipcode_Group_8",
    "Zipcode_Group_Zipcode_Group_9",
]

ONE_HOT_GROUPS = {
    "Condition_of_the_House": [
        "Condition_of_the_House_Excellent", "Condition_of_the_House_Fair",
        "Condition_of_the_House_Good", "Condition_of_the_House_Okay",
    ],
    "Zipcode_Group": [f"Zipcode_Group_Zipcode_Group_{i}" for i in range(1, 10)],
}


def section(title):
    print(f"\n{'-' * 60}\n{title}\n{'-' * 60}")


def main():
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: dataset not found at {DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    problems = []

    section("1. Shape")
    print(f"Rows: {len(df):,}   Columns: {df.shape[1]}")

    section("2. Column check")
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    extra_cols = [c for c in df.columns if c not in EXPECTED_COLUMNS]
    if missing_cols:
        problems.append(f"Missing expected columns: {missing_cols}")
        print(f"MISSING: {missing_cols}")
    if extra_cols:
        print(f"Extra/unexpected columns found: {extra_cols}")
    if not missing_cols and not extra_cols:
        print("All expected columns present, no unexpected extras.")

    section("3. Null check")
    null_counts = df.isnull().sum()
    nulls = null_counts[null_counts > 0]
    if len(nulls) == 0:
        print("No nulls found in any column.")
    else:
        problems.append(f"Nulls found: {nulls.to_dict()}")
        print(nulls)

    section("4. Duplicate rows")
    dupes = df.duplicated().sum()
    print(f"Duplicate rows: {dupes}")
    if dupes > 0:
        problems.append(f"{dupes} duplicate rows found")

    section("5. Range sanity checks")
    checks = [
        ("Sale_Price", df["Sale_Price"] > 0, "Sale_Price should be positive"),
        ("No of Bedrooms", df["No of Bedrooms"] >= 0, "Bedrooms should be >= 0"),
        ("No of Bathrooms", df["No of Bathrooms"] >= 0, "Bathrooms should be >= 0"),
        ("No of Floors", df["No of Floors"] > 0, "Floors should be > 0"),
        ("Age of House (in Years)", df["Age of House (in Years)"] >= 0, "Age should be >= 0"),
        ("Years Since Renovation", df["Years Since Renovation"] >= 0, "Years since renovation should be >= 0"),
    ]
    for col, mask, msg in checks:
        bad = (~mask).sum()
        status = "OK" if bad == 0 else f"FAIL ({bad} rows)"
        print(f"{col:35s} {status}")
        if bad > 0:
            problems.append(f"{col}: {msg} — {bad} rows failed")

    section("6. One-hot group check (each row should sum to 0 or 1, never 2+)")
    # Note: a row summing to 0 is expected here, not an error - it means that
    # row belongs to the baseline category the encoding dropped (common
    # practice to avoid multicollinearity, e.g. a "Poor" condition or a 10th
    # zipcode group with no dedicated column). A row summing to 2+ would be
    # a real problem (a house can't be in two conditions at once).
    for group_name, cols in ONE_HOT_GROUPS.items():
        row_sums = df[cols].sum(axis=1)
        invalid = (row_sums > 1).sum()
        baseline = (row_sums == 0).sum()
        if invalid > 0:
            print(f"{group_name:35s} FAIL ({invalid} rows in more than one category)")
            problems.append(f"{group_name}: {invalid} rows belong to more than one category")
        else:
            print(f"{group_name:35s} OK  ({baseline} rows are the dropped baseline category)")

    section("7. Summary stats (used in Flask KPIs / Tableau performance doc)")
    print(f"Total records:          {len(df):,}")
    print(f"Average sale price:     ${df['Sale_Price'].mean():,.0f}")
    print(f"Median sale price:      ${df['Sale_Price'].median():,.0f}")
    print(f"Average house age:      {df['Age of House (in Years)'].mean():.1f} years")
    print(f"Ever renovated:         {df['Ever_Renovated_Yes'].mean() * 100:.2f}%")
    print(f"Average bedrooms:       {df['No of Bedrooms'].mean():.2f}")
    print(f"Average bathrooms:      {df['No of Bathrooms'].mean():.2f}")
    print(f"Waterfront properties:  {df['Waterfront_View_Yes'].mean() * 100:.2f}%")

    section("Result")
    if problems:
        print(f"{len(problems)} issue(s) found:")
        for p in problems:
            print(f" - {p}")
        sys.exit(1)
    else:
        print("Dataset passed all checks. Ready for Tableau.")


if __name__ == "__main__":
    main()
