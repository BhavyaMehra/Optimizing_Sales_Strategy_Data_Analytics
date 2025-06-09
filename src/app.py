import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Optimizing Sales Strategies Dashboard", layout="wide")

#--- Custom CSS for grey background ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title and Description
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0.3em;'>Optimizing Sales Strategies Dashboard</h1>
    <div style='text-align: center; font-size: 1.1em; max-width: 800px; margin: 0 auto 1.5em auto;'>
        <b>What is this?</b><br>
        This dashboard helps a US-based company selling pens and printers discover which sales approach—<b>Email</b>, <b>Call</b>, or <b>Email + Call</b>—works best to boost revenue and customer engagement.<br><br>
        <b>Why does it matter?</b><br>
        Calls take 30 minutes per customer, emails are instant, and Email + Call means a quick 10-minute follow-up call after an email (saving 20 minutes per customer compared to call-only).<br><br>
        <b>What will you see?</b><br>
        Data cleaning steps, sales method popularity, state-wise revenue, sales trends, and which method brings in the most revenue per customer.
    </div>
    <hr style='margin-bottom: 1.5em;'>
    """,
    unsafe_allow_html=True
)

# --- Load Cleaned Data ---
df = pd.read_csv(r"data/cleaned_product_sales.csv")

# --- Data Cleaning & Feature Engineering ---
col1, col2 = st.columns([1, 2])
with col1:
    st.header("Data Cleaning & Feature Engineering")
    st.markdown("""
    <ul>
        <li>Fixed typos in <b>sales_method</b> so only three categories remain: Email, Call, Email + Call.</li>
        <li>Filled in missing <b>revenue</b> values using the median (about 7% missing, revenue is right-skewed).</li>
        <li>Kept high revenue values—they reflect bulk purchases, not errors.</li>
        <li>Capped <b>years_as_customer</b> at 41 (company founded in 1984, so max tenure is 41 in 2025).</li>
        <li>Found outliers in <b>nb_site_visits</b> but kept them, as most are valid and rare.</li>
        <li>No changes to <b>state</b> (no missing values, 50 unique states).</li>
        <li>Calculated <b>Revenue per Customer</b> for each sales method.</li>
    </ul>
    """, unsafe_allow_html=True)

# --- Sales Volume Distribution (Pie Chart, new color scheme) ---
with col2:
    st.header("Sales Volume Distribution by Method")
    method_counts = df['sales_method'].value_counts().reset_index()
    method_counts.columns = ['Sales Method', 'Count']
    fig_method = px.pie(method_counts, values='Count', names='Sales Method', color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig_method, use_container_width=True)

# --- Pareto Chart: Top 10 States by Revenue & Cumulative % ---
st.header("Top 10 States by Revenue & Cumulative % (Pareto Chart)")
state_revenue = df.groupby("state")["revenue"].sum().sort_values(ascending=False).reset_index()
top10 = state_revenue.head(10).copy()
top10["cumulative_pct"] = top10["revenue"].cumsum() / state_revenue["revenue"].sum() * 100

import plotly.graph_objects as go
fig_pareto = go.Figure()
fig_pareto.add_bar(
    x=top10["state"],
    y=top10["revenue"],
    name="Revenue",
    marker_color="#636EFA"
)
fig_pareto.add_trace(
    go.Scatter(
        x=top10["state"],
        y=top10["cumulative_pct"],
        name="Cumulative %",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#EF553B", width=3)
    )
)
fig_pareto.update_layout(
    title="Pareto Chart: Revenue & Cumulative % by Top 10 States",
    xaxis_title="State",
    yaxis=dict(title="Revenue ($)", showgrid=False),
    yaxis2=dict(title="Cumulative % of Total Revenue", overlaying="y", side="right", range=[0, 100]),
    legend=dict(x=0.01, y=0.99),
    bargap=0.2
)
st.plotly_chart(fig_pareto, use_container_width=True)

# --- Sales Trends Across Marketing Methods ---
col5, col6 = st.columns(2)
with col5:
    st.header("Sales Trends by Method")
    df_grouped = df.groupby(["week", "sales_method"])["revenue"].sum().reset_index()
    fig_trend = px.line(df_grouped, x="week", y="revenue", color="sales_method", markers=True,
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        title="Revenue Trends Over Weeks by Sales Method")
    fig_trend.update_layout(yaxis_title="Revenue ($)", xaxis_title="Week Since Launch")
    st.plotly_chart(fig_trend, use_container_width=True)

with col6:
    st.header("Revenue Heatmap by State & Method")
    heatmap_data = df.groupby(['state', 'sales_method'])['revenue'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='state', columns='sales_method', values='revenue').fillna(0)
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='Viridis',
        colorbar=dict(title='Revenue ($)'),
        text=np.round(heatmap_pivot.values, 0),
        texttemplate="%{text}"
    ))
    fig_heatmap.update_layout(title="Revenue by State and Sales Method", xaxis_title="Sales Method", yaxis_title="State")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# --- Revenue per Customer (Key Business Metric) ---
col7, col8 = st.columns(2)
with col7:
    st.header("Key Metric: Revenue per Customer")
    revenue_per_customer = df.groupby("sales_method").agg(
        total_revenue=("revenue", "sum"),
        unique_customers=("customer_id", "nunique")
    ).reset_index()
    revenue_per_customer["revenue_per_customer"] = (revenue_per_customer["total_revenue"] / revenue_per_customer["unique_customers"]).round(2)
    fig_rpc = px.bar(revenue_per_customer, x="sales_method", y="revenue_per_customer", color="revenue_per_customer",
                     color_continuous_scale=px.colors.sequential.Viridis, text="revenue_per_customer",
                     title="Revenue per Customer by Sales Method")
    fig_rpc.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
    fig_rpc.update_layout(yaxis_title="Revenue per Customer ($)", xaxis_title="Sales Method", showlegend=False)
    st.plotly_chart(fig_rpc, use_container_width=True)

with col8:
    st.header("Customer Segmentation by Tenure")
    tenure_bins = [0, 5, 10, 20, 41]
    tenure_labels = ['0-5', '6-10', '11-20', '21+']
    df['tenure_group'] = pd.cut(df['years_as_customer'], bins=tenure_bins, labels=tenure_labels, right=True)
    tenure_counts = df['tenure_group'].value_counts().sort_index().reset_index()
    tenure_counts.columns = ['Tenure Group', 'Customer Count']
    fig_tenure = px.bar(tenure_counts, x='Tenure Group', y='Customer Count', color='Customer Count',
                        color_continuous_scale=px.colors.sequential.Blues, text='Customer Count',
                        title="Customer Segmentation by Tenure")
    fig_tenure.update_traces(textposition='outside')
    fig_tenure.update_layout(yaxis_title="Number of Customers", xaxis_title="Years as Customer", showlegend=False)
    st.plotly_chart(fig_tenure, use_container_width=True)

# --- Key Insights ---
st.markdown("""
<h1 style='text-align:center; margin-bottom: 0.5em;'>Key Insights & Recommendations</h1>
<div style='display: flex; justify-content: center;'>
  <div style='text-align:center; font-size:1.1em; max-width: 700px;'>
    <ul style='display: inline-block; text-align: left;'>
        <li><b>Email + Call</b> yields the highest revenue per customer and saves significant employee time compared to call-only.</li>
        <li>Revenue is concentrated in a few key states; focusing marketing efforts here can maximize returns and growth.</li>
        <li>Customer tenure is diverse; long-tenure customers are valuable for retention and loyalty strategies.</li>
        <li>Tracking <b>Revenue per Customer</b> helps optimize sales efforts and resource allocation for the business.</li>
        <li>Recommendation: Expand Email + Call for high-value customers, refine email-only campaigns, and reduce reliance on call-only sales for better efficiency and results.</li>
    </ul>
    <br>
    <i>For more details and the full project, visit the <a href='https://github.com/BhavyaMehra/Optimizing_Sales_Strategy_Data_Analytics' target='_blank'>GitHub</a>.</i>
  </div>
</div>
""", unsafe_allow_html=True)
