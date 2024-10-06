import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page layout to wide
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('Interactive Trade Data Visualization Dashboard')
st.write("Use the filters below to explore the data interactively.")

# Load fixed CSV file
@st.cache
def load_data():
    # Update the path to your fixed CSV file
    data = pd.read_csv('Imports_Exports_Dataset.csv')
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Ensure Date is in datetime format
    return data

# Load data
df = load_data()

# Adding slicers (filters)
st.sidebar.header('Filter Data')

# Trade Type Filter (Import/Export)
trade_type = st.sidebar.selectbox("Select Trade Type", options=["Both", "Import", "Export"])
if trade_type != "Both":
    df = df[df['Import_Export'] == trade_type]

# Product Category Filter
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Product Categories", options=categories, default=categories)
df = df[df['Category'].isin(selected_categories)]

# Date Dropdown Filter (Converting date to Year or Year-Month format)
df['Year'] = df['Date'].dt.year  # Extract Year
available_years = df['Year'].dropna().unique()  # Get unique years for dropdown
available_years = sorted(available_years)

# Multi-Year Dropdown Selection
selected_years = st.sidebar.multiselect("Select Years", available_years, default=available_years)

# Filter the dataframe based on the selected years
df = df[df['Year'].isin(selected_years)]

# Visualizations
st.subheader("Visualizations")

# Layout for visualizations: Create 2 rows with 2 columns in each row
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Plot 1: Import-Export Value Distribution (Box Plot)
with col1:
  #  st.write("1. Import-Export Value Distribution")
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='Import_Export', y='Value', data=df)
    plt.title('Import-Export Value Distribution')
    plt.xlabel('Trade Type')
    plt.ylabel('Trade Value (in millions)')
    plt.grid(True)
    st.pyplot(plt.gcf())

# Plot 2: Trade Balance Over Time (Line Plot)
with col2:
   # st.write("2. Trade Balance Over Time")
    df['Trade_Balance'] = df.apply(lambda row: row['Value'] if row['Import_Export'] == 'Export' else -row['Value'], axis=1)
    trade_balance_year = df.groupby('Date')['Trade_Balance'].sum()
    
    plt.figure(figsize=(6, 4))
    sns.lineplot(x=trade_balance_year.index, y=trade_balance_year.values, marker='o')
    plt.title('Trade Balance Over Time')
    plt.xlabel('Year')
    plt.ylabel('Trade Balance (in millions)')
    plt.grid(True)
    st.pyplot(plt.gcf())

# Plot 3: Top 10 Products by Import and Export (Bar Plot)
with col3:
   # st.write("3. Top 10 Products by Import and Export")
    top_products = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack().nlargest(10, 'Export')

    plt.figure(figsize=(6, 4))
    top_products.plot(kind='bar')
    plt.title('Top 10 Products: Import vs Export')
    plt.xlabel('Product Category')
    plt.ylabel('Total Trade Value (in millions)')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt.gcf())

# Plot 4: Distribution of Trade by Product Category (Pie Chart)
with col4:
    #st.write("4. Distribution of Trade by Product Category")
    category_distribution = df.groupby('Category')['Value'].sum().sort_values(ascending=False)

    plt.figure(figsize=(6, 4))
    category_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Trade Distribution by Product Category')
    plt.ylabel('')  # Hide the y-label for a cleaner look
    st.pyplot(plt.gcf())

# Final row: Trade Deficit by Category (Bar Plot)
#st.subheader("Top 10 Categories Contributing to Trade Deficit")
category_trade = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack()
category_trade['Trade_Deficit'] = category_trade['Import'] - category_trade['Export']

trade_deficit_categories = category_trade.sort_values(by='Trade_Deficit', ascending=False)

# Full-width plot for the trade deficit
plt.figure(figsize=(12, 6))
trade_deficit_categories['Trade_Deficit'].nlargest(10).plot(kind='bar', color='lightcoral')
#plt.title('Top 10 Categories Contributing to Trade Deficit')
plt.xlabel('Product Category')
plt.ylabel('Trade Deficit (in millions)')
plt.grid(True)
st.pyplot(plt.gcf())
