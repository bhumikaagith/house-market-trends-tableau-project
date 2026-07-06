# Visualizing Housing Market Trends: An Analysis of Sale Prices and Features using Tableau

Analysis of 21,609 residential property sales, examining how house age, renovation
history, bedrooms, bathrooms, floors, and basement area relate to sale price. Built in
Tableau, published to Tableau Public, and embedded in a small Flask web app.

## What's in this repo

```
housing-market-tableau/
├── data/
│   ├── Transformed_Housing_Data2.csv   # source dataset (21,609 rows x 31 cols)
│   └── DATA_DICTIONARY.md              # column definitions
├── scripts/
│   └── data_validation.py              # checks nulls/dtypes/ranges, prints summary stats
├── tableau/
│   ├── CALCULATED_FIELDS.md            # every calculated field + exact formula
│   └── TABLEAU_STEPS.md                # step-by-step build guide (connect -> publish)
├── flask_app/
│   ├── app.py                          # Flask server (reads the CSV for live KPIs)
│   ├── templates/
│   │   ├── index.html                  # landing page
│   │   └── dashboard.html              # embedded Tableau dashboard/story
│   ├── static/style.css                # lime green + fuchsia pink theme
│   └── requirements.txt
└── README.md
```

## How to use this repo

0. **Validate the data first (optional but recommended)**:
   ```bash
   python scripts/data_validation.py
   ```
   Checks row/column counts, nulls, dtypes, value ranges, and duplicate rows, and
   prints the summary stats referenced elsewhere in this repo. Note: it will flag
   two large groups of rows where all the one-hot columns are 0 (`House Condition`
   and `Zipcode Group`) — that's expected, not an error. See the note at the top
   of `tableau/CALCULATED_FIELDS.md` fields 1 and 4.
1. **Tableau side** — follow `tableau/TABLEAU_STEPS.md` top to bottom. It tells you
   exactly what to connect, which calculated fields to paste in (from
   `tableau/CALCULATED_FIELDS.md`), which charts to build, how to lay out the
   dashboard + story, and how to publish to Tableau Public.
2. **Get your embed link** — once published, Tableau Public gives you a share link
   like `https://public.tableau.com/views/YourWorkbook/Dashboard1`. Copy it.
3. **Web side** — paste that link into `flask_app/app.py` (one line, marked clearly)
   and run the Flask app. It shows the live KPIs computed from the CSV plus the
   embedded Tableau dashboard and story.

## Quick start (Flask app)

```bash
cd flask_app
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

## Dataset

King County–style residential sales data, already cleaned/transformed (no nulls,
categorical fields one-hot encoded). See `data/DATA_DICTIONARY.md` for column
meanings. Source columns include sale price, bedrooms, bathrooms, floors, flat area,
lot area, basement area, house age, years since renovation, condition, waterfront
view, and zipcode group.

## Tech

- **Tableau Desktop / Tableau Public** — all visualizations, dashboard, story
- **Flask (Python)** — thin web wrapper that embeds the published dashboard
- **pandas** — used inside the Flask app only to surface live summary numbers
