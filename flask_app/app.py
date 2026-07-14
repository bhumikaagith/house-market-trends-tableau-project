import os
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# ------------------------------------------------------------------
# PASTE YOUR PUBLISHED TABLEAU PUBLIC LINKS HERE (from Step 7 in
# tableau/TABLEAU_STEPS.md). Leave as-is and the page will show a
# placeholder notice instead of erroring out.
# ------------------------------------------------------------------
TABLEAU_DASHBOARD_URL = "https://public.tableau.com/views/HousingMarketAnalysisDashboard_17837934277010/Dashboard1"
TABLEAU_STORY_URL = "https://public.tableau.com/views/HousingMarketAnalysisDashboard_17837934277010/Story1"
# ------------------------------------------------------------------

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Transformed_Housing_Data2.csv")


def load_kpis():
    df = pd.read_csv(DATA_PATH)
    return {
        "total_sales": f"{len(df):,}",
        "avg_price": f"${df['Sale_Price'].mean():,.0f}",
        "avg_age": f"{df['Age of House (in Years)'].mean():.0f}",
        "renovated_pct": f"{df['Ever_Renovated_Yes'].mean() * 100:.1f}%",
        "avg_bedrooms": f"{df['No of Bedrooms'].mean():.1f}",
        "avg_bathrooms": f"{df['No of Bathrooms'].mean():.1f}",
    }


@app.route("/")
def index():
    return render_template("index.html", kpis=load_kpis())


@app.route("/dashboard")
def dashboard():
    is_placeholder = "YOUR_WORKBOOK" in TABLEAU_DASHBOARD_URL
    return render_template(
        "dashboard.html",
        dashboard_url=TABLEAU_DASHBOARD_URL,
        story_url=TABLEAU_STORY_URL,
        is_placeholder=is_placeholder,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
