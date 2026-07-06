# Calculated Fields — copy these exactly into Tableau

In Tableau: right-click in the Data pane -> **Create Calculated Field** -> paste the
formula -> name it exactly as the heading below -> OK.

Build them in this order (some are used inside later ones).

---

### 1. House Condition
Collapses the 4 one-hot condition columns into one dimension. Note: 30 rows have
all four columns at 0 - that's not missing data, it's the baseline category
dropped during one-hot encoding (standard practice to avoid multicollinearity),
most likely "Poor" condition. Labelled as such below rather than "Unknown."
```
CASE
WHEN [Condition_of_the_House_Excellent] = 1 THEN "Excellent"
WHEN [Condition_of_the_House_Good] = 1 THEN "Good"
WHEN [Condition_of_the_House_Okay] = 1 THEN "Okay"
WHEN [Condition_of_the_House_Fair] = 1 THEN "Fair"
ELSE "Poor (baseline)"
END
```

### 2. Renovation Status
```
IF [Ever_Renovated_Yes] = 1 THEN "Renovated" ELSE "Not Renovated" END
```

### 3. Waterfront View
```
IF [Waterfront_View_Yes] = 1 THEN "Waterfront" ELSE "No Waterfront" END
```

### 4. Zipcode Group
Note: 4,383 rows (about 20% of the data) have all nine columns at 0 - again the
dropped baseline category, not missing data. That's a large enough share that
it's worth its own explicit label rather than folding it into "Unknown."
```
CASE
WHEN [Zipcode_Group_Zipcode_Group_1] = 1 THEN "Group 1"
WHEN [Zipcode_Group_Zipcode_Group_2] = 1 THEN "Group 2"
WHEN [Zipcode_Group_Zipcode_Group_3] = 1 THEN "Group 3"
WHEN [Zipcode_Group_Zipcode_Group_4] = 1 THEN "Group 4"
WHEN [Zipcode_Group_Zipcode_Group_5] = 1 THEN "Group 5"
WHEN [Zipcode_Group_Zipcode_Group_6] = 1 THEN "Group 6"
WHEN [Zipcode_Group_Zipcode_Group_7] = 1 THEN "Group 7"
WHEN [Zipcode_Group_Zipcode_Group_8] = 1 THEN "Group 8"
WHEN [Zipcode_Group_Zipcode_Group_9] = 1 THEN "Group 9"
ELSE "Group 10 (baseline)"
END
```

### 5. House Age Group
Bins `Age of House (in Years)` for cleaner axes.
```
CASE
WHEN [Age of House (in Years)] <= 10 THEN "0-10 yrs"
WHEN [Age of House (in Years)] <= 25 THEN "11-25 yrs"
WHEN [Age of House (in Years)] <= 50 THEN "26-50 yrs"
WHEN [Age of House (in Years)] <= 75 THEN "51-75 yrs"
ELSE "75+ yrs"
END
```

### 6. Renovation Recency Group
Bins `Years Since Renovation`, used for the "Total Sales by Years Since Renovation" chart.
```
CASE
WHEN [Ever_Renovated_Yes] = 0 THEN "Never Renovated"
WHEN [Years Since Renovation] <= 10 THEN "0-10 yrs ago"
WHEN [Years Since Renovation] <= 20 THEN "11-20 yrs ago"
WHEN [Years Since Renovation] <= 30 THEN "21-30 yrs ago"
ELSE "30+ yrs ago"
END
```

### 7. Bathroom Group
Bathrooms come as decimals (1.0, 2.25, 2.5...); this buckets them for a clean axis.
```
CASE
WHEN [No of Bathrooms] <= 1 THEN "1 or fewer"
WHEN [No of Bathrooms] <= 2 THEN "1.25 - 2"
WHEN [No of Bathrooms] <= 3 THEN "2.25 - 3"
ELSE "3.25+"
END
```

### 8. Price per Sqft
Optional, adds a normalized value metric.
```
[Sale_Price] / [Flat Area (in Sqft)]
```

### 9. Avg Sale Price (reference measure)
Not required as a calc field — just drag `Sale_Price` to a shelf and set
Measure = **Average**. Listed here only so it's not missed when counting
"number of calculation fields used" (fields 1-8 above are the 8 calculated fields
for that requirement; this one is a standard aggregation, not a calc field).

---

## Summary for the project checklist
- **No. of Calculation Fields: 8** (House Condition, Renovation Status, Waterfront
  View, Zipcode Group, House Age Group, Renovation Recency Group, Bathroom Group,
  Price per Sqft)
- Built-in field used as-is: **Number of Records** (Tableau auto-generates this on
  data load — used for the "Count of Transformed_Housing_Data" KPI)
