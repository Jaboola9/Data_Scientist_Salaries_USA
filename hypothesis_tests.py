
"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject \
the null hypothesis" depending on the specified alpha
"""

import pandas as pd
from scipy import stats
import scikit_posthocs as ph
import matplotlib.pyplot as plt
import statsmodels.api as sm


def hypothesis_test_one(cleaned_data, alpha=0.05):
    """
    Hypothesis Test One
    H0: The mean salary of all roles are equal \
    H1: The mean salary of at least one role is different
    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    return non_parametric_hypothesis_test_years(cleaned_data, 'role')


def hypothesis_test_two(cleaned_data, alpha=0.05):
    """
    Hypothesis Test One
    H0: The mean salary of all regions are equal \
    H1: The mean salary of at least one roll is different

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    # Get data for tests
    return non_parametric_hypothesis_test_years(cleaned_data, 'region')


def slice_by_year(df, year):
    """
    Return slice of cleaned data by year specified
    """
    slice_df = df[df['year'] == year]
    return slice_df


def descriptive_stats(df):
    """
    Displays descriptive statistics for both categorical and \
    non-categorical data
    """
    display(df.describe().T)
    categoricals = list(df.select_dtypes(include=['object']).columns)
    for column in categoricals:
        print("The most common values in " + column + ":",
              df[column].value_counts()[:5])
        print("The least common values in " + column + ":",
              df[column].value_counts()[-5:])


def stack_df(df, column, values_list):
    """
    Returns a dataframe including entries with only the select values\
    in selected columns
    """
    values_dfs = []
    for value in values_list:
        value_df = df[df[column] == value]
        values_dfs.append(value_df)
    return pd.concat(values_dfs)


def focus_data(df):
    """
    Returns focused dataframe with 2017-2019 data
    and the most common four roles ('DATA SCIENTIST,'\
    'SENIOR DATA SCIENTIST,' 'LEAD DATA SCIENTIST,' \
    and 'ASSOCIATE DATA SCIENTIST.
    """
    years = list(df.year.unique())
    recent_years = years[3:6]
    df_recent_years = stack_df(df, 'year', recent_years)
    df_recent_years.columns
    dropped_columns = ['company',
                       'location',
                       'startdate',
                       'status',
                       'submitdate']
    df_focused = df_recent_years.drop(labels=dropped_columns, axis=1)
    top_4_roles = list(df_focused.role.unique())[0:3]
    top_4_roles.append(df_focused.role.unique()[5])
    top_4_focused = stack_df(df_focused, 'role', top_4_roles)
    return top_4_focused


def describe_dependent_by_year_and_group(df, y_var, x_var, x_var_2=None):
    """
    Get granular descriptive statistics of the dependent variable \
    organized by one or two independent variables
    """
    years = list(df['year'].unique())
    for year in years:
        year_df = slice_by_year(df, year)
        print(year)
        if x_var_2 is None:
            display(year_df.groupby([x_var])[y_var].describe())
        else:
            display(year_df.groupby([x_var, x_var_2])[y_var].describe())


def homogeneity_test_4_groups(df, y_var, x_var):
    """
    Tests 5th assumption that variances of a continuous variable (y_var) \
    are roughly equal accross 4 groups within a categorical variable (x_var) \
    using a Levene test
    """
    groups = list(df[x_var].unique())
    print(x_var)
    return stats.levene(df[y_var][df[x_var] == groups[0]],
                        df[y_var][df[x_var] == groups[1]],
                        df[y_var][df[x_var] == groups[2]],
                        df[y_var][df[x_var] == groups[3]])


def homogenity_test_years(df):
    """
    Performs homogeneity_test_4_groups for each year of the dataset \
    using salary as the continuous variable and role and region as the
    two categorical variables
    """
    years = list(df['year'].unique())
    for year in years:
        df_year = slice_by_year(df, year)
        print(year)
        print(homogeneity_test_4_groups(df_year, 'salary', 'role'))
        print(homogeneity_test_4_groups(df_year, 'salary', 'region'))


def normality_test_4_groups(df, y_var, x_var):
    """
    Tests 6th assumption of a normal distribution of a continuous \
    variables (y_var) are roughly equal accross groups within a \
    categorical variable (x_var) using Shapiro-Wilk Test.
    """
    groups = list(df[x_var].unique())
    for group in groups:
        print(group)
        shapiro_test = stats.shapiro(df[y_var][df[x_var] == group])
        p_value = shapiro_test[1]
        print(f"Shapiro-Wilk test")
        if p_value > 0.05:
            print(f"p-value={p_value}, SATISFIES #5.")
        else:
            print(f"p-value={p_value}, DOES NOT satisfy #5.")


def normality_test_years(df):
    """
    Performs normality_test_4_groups for each year of the dataset \
    using salary as the continuous variable and role and region as the
    two categorical variables
    """
    years = list(df['year'].unique())
    for year in years:
        df_year = slice_by_year(df, year)
        print(year)
        print(normality_test_4_groups(df_year, 'salary', 'role'))
        print(normality_test_4_groups(df_year, 'salary', 'region'))


def non_parametric_hypothesis_test_4_groups(df, y_var, x_var):
    """
    Performs non-parametric Kruskal-Wallis Test to find if there \
    is a significant difference between a continuous variable (y_var) across \
    4 groups of a categorical variable (x_var)
    """
    groups = list(df[x_var].unique())
    print(x_var)
    stat, p = stats.kruskal(df[y_var][df[x_var] == groups[0]],
                            df[y_var][df[x_var] == groups[1]],
                            df[y_var][df[x_var] == groups[2]],
                            df[y_var][df[x_var] == groups[3]])
    print('Statistics = %.3f, p = %.2f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distributions (fail to reject H0) \n')
    else:
        print('Different distributions (reject H0) \n')


def non_parametric_hypothesis_test_years(df, x_var):
    """
    Performs non_parametric_test_4_groups for each year of the dataset \
    using salary as the continuous variable with the x_var selecting \
    categorical
    """
    years = list(df['year'].unique())
    for year in years:
        df_year = slice_by_year(df, year)
        print(f"Kruskal-Wallis Test results for {year}'s data:")
        print(non_parametric_hypothesis_test_4_groups(df_year,
                                                      'salary', x_var))


def posthoc_test_years(df, y_var, x_var):
    """
    Performs Conover-Iman posthoc test for the non-parametric \
    Kruskal-Wallis to find which groups have significant differences \
    (score above 0.05)
    """
    years = list(df['year'].unique())
    for year in years:
        print(year)
        df_year = slice_by_year(df, year)
        display(ph.posthoc_conover(df_year,
                                   val_col=y_var,
                                   group_col=x_var,
                                   p_adjust='holm').round(3))


def qq_test_4_groups(df, y_var, x_var):
    """
    Visually tests 6th assumption of a normal distribution of a \
    continuous variables (y_var) are roughly equal accross groups \
    within a categorical variable (x_var) using using quantile-quantile \
    plots
    """
    groups = list(df[x_var].unique())
    print(x_var)
    sm.qqplot(df[y_var][df[x_var] == groups[0]], fit=True, line='45')
    sm.qqplot(df[y_var][df[x_var] == groups[0]], fit=True, line='45')
    sm.qqplot(df[y_var][df[x_var] == groups[0]], fit=True, line='45')
    sm.qqplot(df[y_var][df[x_var] == groups[0]], fit=True, line='45')
    plt.show()


def qq_test_years(df):
    """
    Performs homogeneity_test_4_groups for each year of the dataset \
    using salary as the continuous variable and role and region as the
    two categorical variables
    """
    years = list(df['year'].unique())
    for year in years:
        df_year = slice_by_year(df, year)
        print(year)
        print(qq_test_4_groups(df_year, 'salary', 'role'))
        print(qq_test_4_groups(df_year, 'salary', 'region'))
