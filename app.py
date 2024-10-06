import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the dashboard
st.title('Imports and Exports Data Visualization Dashboard')

# Upload CSV data file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display sample data
    st.subheader("Sample Data")
    st.dataframe(df.head())

    # Show basic dataset information
    st.write(f"Dataset Dimensions: {df.shape}")
    st.write("Column Information:")
    st.write(df.columns)

    # Visualization 1: Line Plot of Trade Balance Over Time
    df['Trade_Balance'] = df.apply(lambda row: row['Value'] if row['Import_Export'] == 'Export' else -row['Value'], axis=1)
    trade_balance_year = df.groupby('Date')['Trade_Balance'].sum()

    st.subheader("Trade Balance Over Time")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=trade_balance_year.index, y=trade_balance_year.values, marker='o')
    plt.title('Trade Balance Over Time', fontsize=15)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Trade Balance (in millions)', fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

    # Visualization 2: Box Plot for Import-Export Value Distribution
    st.subheader("Import-Export Value Distribution")
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Import_Export', y='Value', data=df)
    plt.title('Import-Export Value Distribution', fontsize=15)
    plt.xlabel('Trade Type', fontsize=12)
    plt.ylabel('Trade Value (in millions)', fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

    # Visualization 3: Comparison of Top 10 Products by Import and Export
    st.subheader("Top 10 Products by Export Value")
    top_products = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack().nlargest(10, 'Export')
    top_products.plot(kind='bar', figsize=(12, 6))
    plt.title('Comparison of Import and Export Values for Top 10 Products', fontsize=15)
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Total Trade Value (in millions)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    # Visualization 4: Pie Chart of Trade Distribution by Product Category
    st.subheader("Trade Distribution by Product Category")
    category_distribution = df.groupby('Category')['Value'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 8))
    category_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Trade by Product Category', fontsize=15)
    plt.ylabel('')  # Hides the y-label
    st.pyplot(plt)

    # Visualization 5: Top 10 Categories Contributing to Trade Deficit
    st.subheader("Top 10 Categories Contributing to Trade Deficit")
    category_trade = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack()
    category_trade['Trade_Deficit'] = category_trade['Import'] - category_trade['Export']
    trade_deficit_categories = category_trade.sort_values(by='Trade_Deficit', ascending=False)
    trade_deficit_categories['Trade_Deficit'].nlargest(10).plot(kind='bar', color='lightcoral')
    plt.title('Top 10 Categories Contributing to Trade Deficit', fontsize=15)
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Trade Deficit (in millions)', fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

else:
    st.write("Please upload a CSV file to proceed.")
