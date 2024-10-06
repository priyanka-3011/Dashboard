# Importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

# Streamlit app title
st.title('Imports and Exports Trade Analysis Dashboard')

# Upload Dataset
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Sample Data")
    st.write(df.head())

    # Sample Data Information
    st.write("### Data Info")
    st.write(df.info())

    # Descriptive Statistics
    st.write("### Descriptive Statistics")
    st.write(df[['Quantity', 'Value']].describe())

    # Skewness and Kurtosis
    skewness = df[['Quantity', 'Value']].skew()
    kurtosis = df[['Quantity', 'Value']].kurtosis()
    st.write("#### Skewness")
    st.write(skewness)
    st.write("#### Kurtosis")
    st.write(kurtosis)

    # T-Test: Import vs Export on Quantity
    st.write("### T-Test: Imports vs Exports (Quantity)")
    import_group = df[df['Import_Export'] == 'Import']['Quantity']
    export_group = df[df['Import_Export'] == 'Export']['Quantity']
    t_stat, p_val = stats.ttest_ind(import_group, export_group)
    st.write(f"T-Statistic: {t_stat}, P-Value: {p_val}")

    # Levene’s test for equal variances
    levene_stat, levene_p = stats.levene(import_group, export_group)
    st.write("### Levene's Test for Equal Variances")
    st.write(f"Levene's Statistic: {levene_stat}, P-Value: {levene_p}")

    # Chi-Square Test
    st.write("### Chi-Square Test: Import_Export vs Shipping_Method")
    contingency_table = pd.crosstab(df['Import_Export'], df['Shipping_Method'])
    chi2_stat, p_val, dof, ex = stats.chi2_contingency(contingency_table)
    st.write(f"Chi-Square Statistic: {chi2_stat}, P-Value: {p_val}")

    # Shapiro-Wilk test for normality (Value column)
    st.write("### Shapiro-Wilk Test: Normality of Trade Values")
    shapiro_stat, shapiro_p = stats.shapiro(df['Value'])
    st.write(f"Shapiro-Wilk Statistic: {shapiro_stat}, P-Value: {shapiro_p}")

    # Mann-Whitney U Test (Weight)
    import_weight = df[df['Import_Export'] == 'Import']['Weight']
    export_weight = df[df['Import_Export'] == 'Export']['Weight']
    mannwhitney_stat, mannwhitney_p = stats.mannwhitneyu(import_weight, export_weight)
    st.write("### Mann-Whitney U Test: Weight")
    st.write(f"Statistic: {mannwhitney_stat}, P-Value: {mannwhitney_p}")

    # Linear Regression: Quantity vs Value
    st.write("### Linear Regression: Quantity vs. Value")
    X = df['Quantity']
    y = df['Value']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    st.write(model.summary())

    # Visualizations

    # Trade Balance Over Time
    st.write("## Trade Balance Over Time")
    df['Trade_Balance'] = df.apply(lambda row: row['Value'] if row['Import_Export'] == 'Export' else -row['Value'], axis=1)
    trade_balance_year = df.groupby('Date')['Trade_Balance'].sum()
    plt.figure(figsize=(10,6))
    sns.lineplot(x=trade_balance_year.index, y=trade_balance_year.values, marker='o')
    plt.title('Trade Balance Over Time')
    plt.xlabel('Year')
    plt.ylabel('Trade Balance (in millions)')
    st.pyplot(plt)

    # Import-Export Value Distribution
    st.write("## Import-Export Value Distribution")
    plt.figure(figsize=(8,6))
    sns.boxplot(x='Import_Export', y='Value', data=df)
    plt.title('Import-Export Value Distribution')
    st.pyplot(plt)

    # Top 10 Products by Import/Export
    st.write("## Top 10 Products by Import and Export")
    top_products = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack().nlargest(10, 'Export')
    top_products.plot(kind='bar', figsize=(12,6))
    plt.title('Comparison of Import and Export Values for Top 10 Products')
    st.pyplot(plt)

    # Distribution of Trade by Category (Pie Chart)
    st.write("## Distribution of Trade by Product Category")
    category_distribution = df.groupby('Category')['Value'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10,8))
    category_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Trade by Product Category')
    st.pyplot(plt)

    # Top 10 Categories with the Highest Trade Deficit
    st.write("## Top 10 Categories with the Highest Trade Deficit")
    category_trade = df.groupby(['Category', 'Import_Export'])['Value'].sum().unstack()
    category_trade['Trade_Deficit'] = category_trade['Import'] - category_trade['Export']
    trade_deficit_categories = category_trade.sort_values(by='Trade_Deficit', ascending=False)
    trade_deficit_categories['Trade_Deficit'].nlargest(10).plot(kind='bar', color='lightcoral')
    plt.title('Top 10 Categories Contributing to Trade Deficit')
    st.pyplot(plt)

else:
    st.write("Python project Term 1/Imports_Exports_Dataset.csv")