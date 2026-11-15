from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Retail KPI Dashboard", page_icon="📊", layout="wide")
st.title("📊 Retail Business KPI Dashboard")
st.caption("Rabtech Academy — Task 5 | Streamlit + Plotly")

DATA = Path("data/clean_dataset.csv")

@st.cache_data
def load_data(path):
    d = pd.read_csv(path, low_memory=False)
    if "Order Date" in d:
        d["Order Date"] = pd.to_datetime(d["Order Date"], errors="coerce")
    for c in ["Sales", "Profit", "Quantity", "Discount", "Shipping Cost", "Profit Margin (%)"]:
        if c in d:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    return d

if not DATA.exists():
    st.error("Dataset not found. Copy your Task 4 clean_dataset.csv into the data folder.")
    st.code("rabtech-task-5-dashboard/data/clean_dataset.csv")
    st.stop()

df = load_data(DATA)
if not {"Sales", "Profit"}.issubset(df.columns):
    st.error("This dataset must contain Sales and Profit columns.")
    st.stop()

st.sidebar.header("Filters")
d = df.copy()
if "Order Date" in d and d["Order Date"].notna().any():
    lo, hi = d["Order Date"].min().date(), d["Order Date"].max().date()
    dates = st.sidebar.date_input("Order date range", value=(lo, hi), min_value=lo, max_value=hi)
    if isinstance(dates, tuple) and len(dates) == 2:
        d = d[d["Order Date"].dt.date.between(dates[0], dates[1])]
for col, label in [("Region","Region"),("Segment","Customer segment"),("Category","Product category"),("Country","Country")]:
    if col in d:
        opts = sorted(d[col].dropna().astype(str).unique())
        chosen = st.sidebar.multiselect(label, opts, default=opts)
        if chosen:
            d = d[d[col].astype(str).isin(chosen)]
if d.empty:
    st.warning("No records match these filters.")
    st.stop()

orders = d["Order ID"].nunique() if "Order ID" in d else len(d)
revenue, profit = d["Sales"].sum(), d["Profit"].sum()
aov = revenue / orders if orders else 0
c1,c2,c3,c4 = st.columns(4)
c1.metric("Revenue", f"${revenue:,.2f}")
c2.metric("Total profit", f"${profit:,.2f}")
c3.metric("Unique orders", f"{orders:,}")
c4.metric("Average order value", f"${aov:,.2f}")
st.caption("AOV = sales divided by distinct Order IDs. Each dataset row is an order line, not necessarily a whole order.")
with st.expander("CAC and churn-rate data limitation"):
    st.write("Customer Acquisition Cost requires acquisition/marketing spend and newly acquired customer counts. Churn rate requires customer status or retention-period data. These fields are not present in this transaction dataset, so they are not fabricated.")

st.divider()
left,right = st.columns(2)
with left:
    st.subheader("Monthly revenue trend")
    if "Order Date" in d and d["Order Date"].notna().any():
        t = d.dropna(subset=["Order Date"]).copy()
        t["Month"] = t["Order Date"].dt.to_period("M").astype(str)
        m = t.groupby("Month", as_index=False)[["Sales","Profit"]].sum()
        st.plotly_chart(px.area(m,x="Month",y="Sales",title="Revenue by month"),use_container_width=True)
        st.plotly_chart(px.line(m,x="Month",y="Profit",markers=True,title="Profit by month"),use_container_width=True)
    else:
        st.info("Order Date is not available for trend analysis.")
with right:
    st.subheader("Category and segment")
    if "Category" in d:
        cat = d.groupby("Category",as_index=False)["Sales"].sum()
        st.plotly_chart(px.bar(cat,x="Category",y="Sales",color="Category",title="Revenue by category"),use_container_width=True)
    if "Segment" in d:
        seg = d.groupby("Segment",as_index=False)["Sales"].sum()
        st.plotly_chart(px.pie(seg,names="Segment",values="Sales",hole=.4,title="Revenue by segment"),use_container_width=True)

st.divider()
st.subheader("Geographic revenue view")
if "Country" in d:
    geo = d.groupby("Country",as_index=False)["Sales"].sum()
    fig = px.choropleth(geo,locations="Country",locationmode="country names",color="Sales",
                        hover_name="Country",title="Revenue by country",color_continuous_scale="Blues")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(geo.sort_values("Sales",ascending=False),use_container_width=True,hide_index=True)
elif "State" in d:
    geo = d.groupby("State",as_index=False)["Sales"].sum().sort_values("Sales",ascending=False).head(20)
    st.plotly_chart(px.bar(geo,x="State",y="Sales",title="Top states by revenue"),use_container_width=True)
else:
    st.info("No geographic field found in the dataset.")

x,y = st.columns(2)
with x:
    st.subheader("Profit by category")
    if "Category" in d:
        p = d.groupby("Category",as_index=False)["Profit"].sum()
        st.plotly_chart(px.bar(p,x="Category",y="Profit",color="Profit"),use_container_width=True)
with y:
    st.subheader("Discount vs profit")
    if {"Discount","Profit"}.issubset(d.columns):
        s = d[["Discount","Profit"]].dropna()
        if len(s)>5000: s=s.sample(5000,random_state=42)
        st.plotly_chart(px.scatter(s,x="Discount",y="Profit",opacity=.45),use_container_width=True)

st.subheader("Filtered data preview")
st.dataframe(d.head(100),use_container_width=True)
st.caption(f"Showing up to 100 of {len(d):,} filtered rows.")
