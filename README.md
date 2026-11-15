# Rabtech Academy — Task 5: Interactive Dashboard & KPI Visualizations

Interactive retail dashboard built with Streamlit, Pandas and Plotly using the cleaned Global Superstore dataset from Task 3/4.

## Features
- Revenue, total profit, distinct orders and average order value (AOV) KPI cards.
- Monthly revenue area chart and monthly profit trend.
- Revenue by category and customer segment.
- Country-level geographic revenue choropleth when country names are recognized.
- Interactive date, region, segment, category and country filters.
- Discount-versus-profit scatter plot and filtered data preview.

## KPI limitation
The transaction dataset does not contain acquisition/marketing spend or customer churn/subscription status. CAC and churn rate therefore cannot be calculated reliably and are identified as unavailable rather than invented.

## Dataset setup
Copy the Task 4 cleaned file to `data/clean_dataset.csv`.

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Structure
```text
rabtech-task-5-dashboard/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── clean_dataset.csv  # copy your Task 4 dataset here
```
