# Data Dictionary — Transformed_Housing_Data2.csv

21,609 rows x 31 columns. No missing values. One row = one house sale.

| Column | Type | Description |
|---|---|---|
| `Sale_Price` | float | Sale price in USD |
| `No of Bedrooms` | int | Bedroom count |
| `No of Bathrooms` | float | Bathroom count (0.25 increments = half/quarter baths) |
| `Flat Area (in Sqft)` | float | Living area, sqft |
| `Lot Area (in Sqft)` | float | Total lot size, sqft |
| `No of Floors` | float | Floor count |
| `No of Times Visited` | int | Times the listing was viewed pre-sale (0-4) |
| `Overall Grade` | int | Construction/design grade, 1 (low) - 13 (high) |
| `Area of the House from Basement (in Sqft)` | float | Above-ground living area, sqft |
| `Basement Area (in Sqft)` | int | Basement area, sqft (0 = no basement) |
| `Age of House (in Years)` | int | Years since built, at time of sale |
| `Latitude` / `Longitude` | float | Property coordinates |
| `Living Area after Renovation (in Sqft)` | float | Living area of nearby comparable homes |
| `Lot Area after Renovation (in Sqft)` | int | Lot area of nearby comparable homes |
| `Years Since Renovation` | int | Years since last renovation (0 = never renovated / renovated in sale year) |
| `Condition_of_the_House_*` | int (0/1) | One-hot: Excellent / Fair / Good / Okay |
| `Ever_Renovated_Yes` | int (0/1) | 1 = house has been renovated |
| `Waterfront_View_Yes` | int (0/1) | 1 = has waterfront view |
| `Zipcode_Group_Zipcode_Group_1..9` | int (0/1) | One-hot: which of 9 zipcode clusters |

## Notes for Tableau

The condition, renovation, waterfront, and zipcode fields are **one-hot encoded**
(spread across multiple 0/1 columns) rather than single text columns. `tableau/CALCULATED_FIELDS.md`
collapses each group back into one readable dimension (e.g. a single `House Condition`
field with values Excellent/Good/Okay/Fair) so they work cleanly as filters and axes.
