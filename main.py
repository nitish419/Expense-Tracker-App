import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App Configuration
st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")
st.title("📊 Expense Tracker & Financial Analytics")

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/synthetic_expenses.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run generate_data.py first.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("Filters")
    selected_month = st.sidebar.multiselect("Select Month", df['Month_Year'].unique(), default=df['Month_Year'].unique())
    selected_category = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
    
    # Sidebar Filters
    st.sidebar.header("Settings")
    # Add a dropdown for the user to pick their currency
    currency = st.sidebar.selectbox("Select Currency", ["₹", "$", "€", "£"])
    
    st.sidebar.markdown("---") # Adds a nice visual line
    
    st.sidebar.header("Filters")
    # ... (keep your existing month and category filters here) ...
    # Apply Filters
    filtered_df = df[(df['Month_Year'].isin(selected_month)) & (df['Category'].isin(selected_category))]

# Top KPIs
    col1, col2, col3 = st.columns(3)
    # Notice how we use {currency} instead of a hardcoded symbol
    col1.metric("Total Expenses", f"{currency}{filtered_df['Amount'].sum():,.2f}")
    col2.metric("Total Transactions", len(filtered_df))
    col3.metric("Average Transaction", f"{currency}{filtered_df['Amount'].mean():,.2f}")

    st.markdown("---")

# Visualizations
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Spending by Category")
        category_spend = filtered_df.groupby('Category')['Amount'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=category_spend, x='Amount', y='Category', palette='viridis', ax=ax)
        # Update the X-axis label dynamically
        ax.set_xlabel(f"Total Amount ({currency})")
        ax.set_ylabel("")
        st.pyplot(fig)

    with col_chart2:
        st.subheader("Monthly Spending Trend")
        monthly_trend = filtered_df.groupby('Month_Year')['Amount'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.lineplot(data=monthly_trend, x='Month_Year', y='Amount', marker='o', color='b', ax=ax2)
        plt.xticks(rotation=45)
        ax2.set_xlabel("Month")
        # Update the Y-axis label dynamically
        ax2.set_ylabel(f"Total Amount ({currency})")
        st.pyplot(fig2)

    # Data Table
    st.subheader("Detailed Transactions")
    st.dataframe(filtered_df.sort_values('Date', ascending=False).head(50)) # Show top 50