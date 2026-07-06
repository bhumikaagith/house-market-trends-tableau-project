# Tableau Build Guide — step by step

Follow in order. Everything you paste in is in `CALCULATED_FIELDS.md`.

---

## 1. Data Collection & Connect

1. Get `data/Transformed_Housing_Data2.csv` from this repo onto your machine
   (already cleaned: 21,609 rows, 31 columns, zero nulls).
2. Open **Tableau Desktop** -> **Connect -> Text File** -> select
   `Transformed_Housing_Data2.csv`.
3. On the connection screen, confirm data types Tableau guessed:
   - `Sale_Price`, `Flat Area (in Sqft)`, `Lot Area (in Sqft)`, `No of Bathrooms`,
     `No of Floors`, `Latitude`, `Longitude` → **Number (decimal)**
   - `No of Bedrooms`, `Age of House (in Years)`, `Years Since Renovation`,
     `Basement Area (in Sqft)`, all the `_Yes`/one-hot columns → **Number (whole)**
4. Rename the data source (bottom tab) to `Housing Data`.
5. Go to **Sheet 1** to leave the data-source screen — you're now ready to build.

## 2. Data Preparation (in Tableau)

1. In the Data pane, drag every `Condition_of_the_House_*`, `Zipcode_Group_*`,
   `Ever_Renovated_Yes`, `Waterfront_View_Yes` field — right-click each →
   confirm they're set as **Dimension** (not Measure); Tableau sometimes reads
   0/1 columns as measures by default.
2. Create the 8 calculated fields from `CALCULATED_FIELDS.md`, in the listed order.
3. After creating them, right-click each new calculated field → **Move to Dimensions**
   if it lands in Measures (text-output CASE/IF fields should auto-sort as dimensions;
   double check `Price per Sqft` sits in Measures since it's numeric).
4. Optional cleanup: right-click `Sale_Price` → **Default Properties → Number Format**
   → Currency (Standard), 0 decimal places. Do the same for `Price per Sqft`.
5. Rename fields for clarity if you want shorter labels in tooltips (right-click →
   Rename): e.g. `Area of the House from Basement (in Sqft)` → `Above-Ground Area (sqft)`.

## 3. Visualizations — build these 6 sheets

Create a new worksheet for each (right-click the sheet tabs at the bottom → New Worksheet).
Rename each tab to match the title below.

### Sheet 1 — "Total Records"
- Drag `Number of Records` (bottom of Data pane, auto-created) to **Text** on the Marks card.
- Show Mark type: **Text/Big Number**. This is the "Count of Transformed_Housing_Data" KPI.

### Sheet 2 — "Avg Sale Price"
- Drag `Sale_Price` to **Text**. Right-click the pill → **Measure → Average**.
- Set number format to Currency (from step 2.4). This is a single-value KPI tile.

### Sheet 3 — "Area from Basement"
- Drag `Area of the House from Basement (in Sqft)` to **Columns**.
- Right-click it → **Create Bins** → bin size ~250.
- Drag the new bin field to **Rows**, drag `Number of Records` to **Rows** as well (or Text).
- Mark type: **Bar**. This shows the distribution of above-ground area.

### Sheet 4 — "Total Sales by Years Since Renovation"
- Drag `Renovation Recency Group` (calc field) to **Columns**.
- Drag `Sale_Price` to **Rows** → set aggregation to **Sum**.
- Mark type: **Bar**. Sort descending (click the sort icon on the axis).
- Optional: add `Renovation Status` to **Color** to visually separate renovated vs not.

### Sheet 5 — "House Age by Renovation Status"
- Drag `Renovation Status` (calc field) to **Columns**.
- Drag `Age of House (in Years)` to **Rows**.
- Change Mark type to **Box Plot**: select both pills → Show Me panel → box-and-whisker.
- This answers "does renovation status affect the age distribution."

### Sheet 6 — "House Age by Bedrooms / Bathrooms / Floors"
Build as three small worksheets that will sit side by side on the dashboard
(Tableau doesn't do 3 independent x-axes in one chart cleanly):
- **6a**: Columns = `No of Bedrooms`, Rows = `Age of House (in Years)` (Avg), Mark = Bar.
- **6b**: Columns = `Bathroom Group` (calc field), Rows = `Age of House (in Years)` (Avg), Mark = Bar.
- **6c**: Columns = `No of Floors`, Rows = `Age of House (in Years)` (Avg), Mark = Bar.
- Give each a distinct color from the palette so they read as a matched set
  (Marks card → Color → pick 3 related hues).

## 4. Dashboard — responsive design

1. Right-click sheet tabs → **New Dashboard**. Name it `Housing Market Overview`.
2. Set **Size** (top of Dashboard pane) to **Automatic** so it adapts to the viewer's
   screen, or build fixed **Desktop**, **Tablet**, **Phone** layouts:
   - Dashboard pane → **Device Preview** (top toolbar) → **Add Phone Layout** /
     **Add Tablet Layout**.
   - On the Phone layout, drag the KPI tiles (Sheets 1-2) to the top, stack the
     charts vertically, and hide the 3-way age chart (6a/6b/6c) or replace with
     just 6a to keep it uncluttered on small screens (use the **Layout → visibility (eye icon)**
     to toggle a sheet's presence per device).
3. Drag onto the Desktop layout:
   - Row 1: Sheet 1 + Sheet 2 (as two small KPI tiles, floating or tiled left-to-right).
   - Row 2: Sheet 4 (Total Sales by Years Since Renovation) and Sheet 3 (Area from Basement)
     side by side.
   - Row 3: Sheet 5 (Age by Renovation Status).
   - Row 4: Sheets 6a, 6b, 6c side by side (three equal-width containers).
4. Add filters that apply across the dashboard:
   - Right-click `Renovation Status` (on any sheet) → **Filters** → drag to dashboard
     → set **Apply to Worksheets → All Using This Data Source**.
   - Repeat for `House Condition`, `Waterfront View`, `Zipcode Group`, and
     `No of Bedrooms` (as a range/slider filter).
   - That gives 5 interactive filters — covers "Utilization of Data Filters."
5. Add a title text box at the top: "Visualizing Housing Market Trends" with a
   one-line subtitle.
6. **Format → Dashboard → set a consistent font/color** so it doesn't look default
   (Format menu → Workbook Theme, or manually match fonts across text boxes).

## 5. Storyboard

1. Right-click sheet tabs → **New Story**. Name it `Housing Market Insights`.
2. Build story points in this sequence (use **Add a caption** on each):
   1. **"21,609 sales analyzed"** — drag Sheet 1 + Sheet 2 (the KPI tiles).
   2. **"Where does the price live?"** — drag Sheet 3 (basement/above-ground area distribution).
   3. **"Renovation barely moves the needle on age"** — drag Sheet 5.
   4. **"Older homes get renovated less often"** — drag Sheet 4.
   5. **"Bigger homes skew older or newer?"** — drag Sheets 6a/6b/6c dashboard.
   6. **"Takeaways"** — a text-only story point summarizing 2-3 findings in plain language.
3. Use the **Navigator** bar styling (Format → Story) to keep captions consistent.
4. Add a **Highlight** action on the renovation story point: select a bar in Sheet 4,
   right-click → **Annotate → Mark**, to call out the peak bucket.

## 6. Performance Testing

Record these numbers somewhere (a text box on the dashboard, or in your project report) —
this is what "Performance Testing" is asking you to document:

| Metric | How to check | Typical value here |
|---|---|---|
| Amount of data loaded | Data Source tab → bottom-left row count | 21,609 rows / 31 columns |
| No. of filters used | Count dashboard filter cards | 5 |
| No. of calculation fields | Data pane → fields with the `=` icon | 8 |
| No. of visualizations/graphs | Sheet tabs used on the dashboard | 8 (Sheets 1,2,3,4,5,6a,6b,6c) |
| Load time | Help → Settings and Performance → **Start Performance Recording**, interact, then **Stop** | note the generated performance workbook's total duration |

If load feels slow: right-click the data source → **Extract** instead of Live
connection (Data → Extract → Compute), which pre-aggregates and speeds up rendering
significantly for a static CSV like this one.

## 7. Publishing to Tableau Public

1. Make sure the dashboard and story both run without errors and unused sheets
   are hidden (right-click sheet tab → **Hide**) to keep the file lean.
2. **File → Save to Tableau Public As...**
3. Sign in (or create a free account at https://public.tableau.com).
4. Give the workbook a name, e.g. `Housing-Market-Trends`, and click **Save**.
   Tableau uploads it and opens your browser to the published page.
5. On that page, click **Share** to copy the link — it looks like:
   `https://public.tableau.com/views/Housing-Market-Trends/HousingMarketOverview`
6. You'll use that exact URL in `flask_app/app.py` in the next step (see the
   `TABLEAU_VIEW_URL` variable at the top of the file).
7. Copy the **Embed Code** shown on the same Share panel too — it's the same URL
   with `?:embed=y` etc, useful as a fallback if you ever want a raw `<iframe>`
   instead of the JS API embed the Flask app uses.
