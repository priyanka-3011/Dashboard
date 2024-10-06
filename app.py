import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

# Title of the dashboard
st.title('Imports and Exports Analysis Dashboard')

# Upload CSV data file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Sample 3001 records based on random state (roll number)
    Sample_data = df.sample(n=3001, random_state=55034)

    # Show sample data
    st.subheader("Sample Data")
    st.dataframe(Sample_data.head())

    # Show dataset dimensions
    st.write(f"Dataset Dimensions: {df.shape}")

    # Descriptive Statistics
    st.subheader("Descriptive Statistics")
    descriptive_stats = df[['Quantity', 'Value']].describe()
    st.write(descriptive_stats)

    skewness = df[['Quantity', 'Value']].skew()
    kurtosis = df[['Quantity', 'Value']].kurtosis()
    st.write("Skewness:", skewness)
    st.write("Kurtosis:", kurtosis)

    # Grouping by Import and Export for statistical tests
    import_group = df[df['Import_Export'] == 'Import']['Quantity']
    export_group = df[df['Import_Export'] == 'Export']['Quantity']

    # T-test
    t_stat, p_val = stats.ttest_ind(import_group, export_group)
    st.write(f"T-Test: t-statistic = {t_stat}, p-value = {p_val}")

    # Levene's Test for equal variances
    levene_stat, levene_p = stats.levene(import_group, export_group)
    st.write(f"Levene's Test: statistic = {levene_stat}, p-value = {levene_p}")

    # Chi-square test
    st.subheader("Chi-Square Test (Import_Export vs Shipping Method)")
    contingency_table = pd.crosstab(df['Import_Export'], df['Shipping_Method'])
    chi2_stat, chi2_p_val, dof, ex = stats.chi2_contingency(contingency_table)
    st.write(f"Chi-Square Test: chi2_stat = {chi2_stat}, p-value = {chi2_p_val}")
    
    # Shapiro-Wilk Test for Normality
    shapiro_stat, shapiro_p = stats.shapiro(df['Value'])
    st.write(f"Shapiro-Wilk Test: statistic = {shapiro_stat}, p-value = {shapiro_p}")

    # Mann-Whitney U Test
    import_weight = df[df['Import_Export'] == 'Import']['Weight']
    export_weight = df[df['Import_Export'] == 'Export']['Weight']
    mannwhitney_stat, mannwhitney_p = stats.mannwhitneyu(import_weight, export_weight)
    st.write(f"Mann-Whitney U Test: statistic = {mannwhitney_stat}, p-value = {mannwhitney_p}")

    # Linear Regression (Quantity vs Value)
    X = df['Quantity']
    y = df['Value']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    st.subheader("Linear Regression: Quantity vs Value")
    st.write(model.summary())

    # Trade Balance Over Time
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

    # Boxplot for Import-Export Value Distribution
    st.subheader("Import-Export Value Distribution")
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Import_Export', y='Value', data=df)
    plt.title('Import-Export Value Distribution', fontsize=15)
    plt.xlabel('Trade Type', fontsize=12)
    plt.ylabel('Trade Value (in millions)', fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

    # Top 10 Products: Comparison of Import and Export Values
    st.subheader("Top 10 Products by Export Value")
    top_products = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack().nlargest(10, 'Export')
    top_products.plot(kind='bar', figsize=(12, 6))
    plt.title('Comparison of Import and Export Values for Top 10 Products', fontsize=15)
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Total Trade Value (in millions)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

    # Pie chart for distribution of trade by category
    st.subheader("Distribution of Trade by Product Category")
    category_distribution = df.groupby('Category')['Value'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 8))
    category_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Trade by Product Category', fontsize=15)
    plt.ylabel('')  # Hides the y-label
    st.pyplot(plt)

    # Trade Deficit Analysis
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