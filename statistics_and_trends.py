"""
This is the template file for the statistics and trends assignment.
You will be expected to complete all the sections and
make this a fully working, documented file.
You should NOT change any function, file or variable names,
 if they are given to you here.
Make use of the functions presented in the lectures
and ensure your code is PEP-8 compliant, including docstrings.
"""
from corner import corner
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns


def plot_relational_plot(df):
    fig, ax = plt.subplots(1, 1, dpi=1000)
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]/1000000000
    ax.scatter(x, y)
    ax.set_title('Comapny Size vs Revenue')
    ax.set_xlabel('Company Size')
    ax.set_ylabel('Revenue (£Billions)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.savefig('relational_plot.png')
    return


def plot_categorical_plot(df):
    fig, ax = plt.subplots(dpi=1000)
    counts = df.iloc[:, 2].value_counts()
    ax.pie(counts, autopct='%1.1f%%', labels=counts.index)
    ax.set_title('Seniority Distribution in Job Listings')
    plt.savefig('categorical_plot.png')
    return


def plot_statistical_plot(df):
    fig, ax = plt.subplots(1, 2, dpi=1000)
    (df.iloc[:, 0]/100000).plot.box(ax=ax[0], grid=False)
    ax[0].set_xlabel('Company Size')
    ax[0].set_ylabel('Number of Employees (100,000)')
    ax[0].set_xticklabels([])

    (df.iloc[:, 1]/1000000000).plot.box(ax=ax[1], grid=False)
    ax[1].set_ylabel('€Billion')
    ax[1].set_xlabel('Revenue')
    ax[1].set_xticklabels([])
    ax[1].set_yscale('log')

    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.savefig('statistical_plot.png')
    return


def statistical_analysis(df, col: str):
    mean = df[col].mean()
    stddev = df[col].std()
    skew = df[col].skew()
    excess_kurtosis = df[col].kurtosis()
    return mean, stddev, skew, excess_kurtosis


def preprocessing(df):
    # You should preprocess your data in this function and
    # make use of quick features such as 'describe', 'head/tail' and 'corr'.
    df = df.loc[:, ['company_size', 'revenue', 'seniority_level']]

    def clean_revenue_data(val):
        if pd.isna(val):
            return None
        s = str(val).replace('€', '').
                     replace(',', '').strip()  # remove € and commas
        multiplier = 1
        if s.upper().endswith('B'):
            multiplier = 1e9
            s = s[:-1]
        elif s.upper().endswith('M'):
            multiplier = 1e6
            s = s[:-1]
        try:
            return float(s) * multiplier
        except ValueError:
            return None

    df['revenue'] = df['revenue'].apply(clean_revenue_data)

    df['company_size'] = pd.to_numeric(df['company_size'].
                                       astype(str).
                                       str.replace(',', ''),
                                       errors='coerce')
    df = df.dropna()
    
    df.head()
    df.describe()
    df.corr(numeric_only=True)
    df.cov(numeric_only=True)
    return df


def writing(moments, col):
    print(f'For the attribute {col}:')
    print(f'Mean = {moments[0]:.2f}, '
          f'Standard Deviation = {moments[1]:.2f}, '
          f'Skewness = {moments[2]:.2f}, and '
          f'Excess Kurtosis = {moments[3]:.2f}.')
    # Delete the following options as appropriate for your data.
    # Not skewed and mesokurtic can be defined with asymmetries <-2 or >2.
    print('The data was right skewed and leptokurtic.')
    return


def main():
    df = pd.read_csv('data.csv')
    df = preprocessing(df)
    col = 'revenue'
    plot_relational_plot(df)
    plot_statistical_plot(df)
    plot_categorical_plot(df)
    moments = statistical_analysis(df, col)
    writing(moments, col)
    return


if __name__ == '__main__':
    main()
