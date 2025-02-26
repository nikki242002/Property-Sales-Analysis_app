import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from datetime import datetime

def main():
    st.set_page_config(page_title="Property Sales Dashboard", layout="wide")

    # --- Load Data ---
    file_path = "Dataset//property_sales_dataset(Cleaned).csv"
    data = pd.read_csv(file_path)
    st.write(data)
    data.dropna(inplace=True)

    # --- Data Processing ---
    data["Profit per Sq Ft"] = data["Revenue"] / data["Area (Sq Ft)"]
    data["Growth Rate"] = data["Revenue"].pct_change().fillna(0)
    if "Yearly Sales" in data.columns:
        data["Yearly Sales"] = pd.to_datetime(data["Yearly Sales"], format="%Y-%m-%d", errors="coerce")
        data["Yearly Sales"] = pd.to_datetime(data["Yearly Sales"], errors="coerce")  
        data["Yearly Sales"] = data["Yearly Sales"].dt.strftime("%Y-%m")
    data["Property Tax Rate"] = np.random.uniform(5, 20, size=len(data))
    data["Property Tax Amount"] = (data["Revenue"] * data["Property Tax Rate"]) / 100

    # --- Aggregated Data ---
    States_metrics = data.groupby("States").agg({
        "Revenue": "sum",
        "Sales": "sum",
        "Growth Rate": "mean",
        "Profit per Sq Ft": "sum",
        "Property Tax Amount": "mean"
    }).reset_index()

    States_tax = data.groupby("States")["Property Tax Amount"].sum().reset_index()

    st.title("🏠 Property Sales Analysis Dashboard")

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")
    selected_state = st.sidebar.selectbox("Select a State:", ["All"] + list(data["States"].unique()))

    # Filter Data
    filtered_data = data if selected_state == "All" else data[data["States"] == selected_state]
    
    # --- Dashboard Layout ---
    col1, col2 = st.columns(2)

    # Theme Toggle
    theme_options = {"Dark": "plotly_dark", "Light": "plotly_white", "Seaborn": "seaborn", "GGplot2": "ggplot2"}
    selected_theme = st.sidebar.radio("Select Theme:", list(theme_options.keys()))
    template = theme_options[selected_theme]
    
    st.title("🏠 Property Sales Analysis Dashboard")
    
    # --- Revenue by State (Bar Chart) ---
    fig_revenue = px.bar(States_metrics, x="States", y="Revenue", color="States",
                         title="📊 Revenue by State", template="plotly_dark")
    col1.plotly_chart(fig_revenue, use_container_width=True)

    # --- Sales vs Revenue (Scatter Plot) ---
    fig_scatter = px.scatter(filtered_data, x="Sales", y="Revenue", color="States",
                             title="💲 Sales vs Revenue", template="plotly_dark", size="Revenue")
    col2.plotly_chart(fig_scatter, use_container_width=True)

    # --- Sales Distribution (Histogram) ---
    fig_sales_hist = px.histogram(data, x="Sales", nbins=20, title="📈 Sales Distribution", template="plotly_dark")
    st.plotly_chart(fig_sales_hist, use_container_width=True)

    # --- Property Tax by State (Pie Chart) ---
    fig_pie = px.pie(States_tax, values="Property Tax Amount", names="States", title="🏦 Property Tax Distribution",
                     template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

    # --- Revenue Distribution (Boxplot) ---
    fig_box = px.box(filtered_data, x="States", y="Revenue", color="States",
                     title="📉 Revenue Distribution", template="plotly_dark")
    st.plotly_chart(fig_box, use_container_width=True)

    # --- Growth Rate Over Time (Line Chart) ---
     filtered_data = filtered_data.sort_values(["Yearly Sales", "States"]) 
     fig_growth = px.line(filtered_data, x="Yearly Sales", y="Growth Rate", color="States", title="📊 Growth Rate Over Time", template=template, markers=True, line_group="States")
     st.plotly_chart(fig_growth, use_container_width=True)

    # --- Summary Metrics ---
    st.sidebar.header("📌 Key Metrics")
    total_revenue = filtered_data["Revenue"].sum()
    avg_growth = filtered_data["Growth Rate"].mean()
    total_sales = filtered_data["Sales"].sum()

    st.sidebar.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    st.sidebar.metric("📈 Avg Growth Rate", f"{avg_growth:.2%}")
    st.sidebar.metric("🛒 Total Sales", f"{total_sales:,}")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.write("Developed by **Nitin Sharma** | Powered by Streamlit & Plotly")

if __name__ == "__main__":
    main()
