"""
pd_viz
==========
A package for visualizing python dataframes
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# some seaborn codes
import seaborn as sns
pal = {'male': "green", 'female': "Pink"}
sns.set(style="darkgrid")
plt.subplots(figsize=(15, 8))
ax = sns.barplot(x="Sex",
                 y="Survived",
                 data=df,
                 palette=pal,
                 linewidth=5,
                 order=['female', 'male'],
                 capsize=.05,
                 )

plt.title("Survived/Non-Survived Passenger Gender Distribution",
          fontsize=25, loc='center', pad=40)
plt.ylabel("% of passenger survived", fontsize=15, )
plt.xlabel("Sex", fontsize=15)

# the plotting_3_chart plots a 3 chart with in one place


def plotting_3_chart(df, feature):
    """

    Parameters
    ----------
    df :
        
    feature :
        

    Returns
    -------

    """
    # Importing seaborn, matplotlab and scipy modules.
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from scipy import stats
    import matplotlib.style as style
    style.use('fivethirtyeight')

    # Creating a customized chart. and giving in figsize and everything.
    fig = plt.figure(constrained_layout=True, figsize=(12, 8))
    # creating a grid of 3 cols and 3 rows.
    grid = gridspec.GridSpec(ncols=3, nrows=3, figure=fig)
    #gs = fig3.add_gridspec(3, 3)

    # Customizing the histogram grid.
    ax1 = fig.add_subplot(grid[0, :2])
    # Set the title.
    ax1.set_title('Histogram')
    # plot the histogram.
    sns.distplot(df.loc[:, feature], norm_hist=True, ax=ax1)

    # customizing the QQ_plot.
    ax2 = fig.add_subplot(grid[1, :2])
    # Set the title.
    ax2.set_title('QQ_plot')
    # Plotting the QQ_Plot.
    stats.probplot(df.loc[:, feature], plot=ax2)

    # Customizing the Box Plot.
    ax3 = fig.add_subplot(grid[:, 2])
    # Set title.
    ax3.set_title('Box Plot')
    # Plotting the box plot.
    sns.boxplot(df.loc[:, feature], orient='v', ax=ax3)

# plotting_3_chart(df, 'SalePrice')


def customized_scatterplot(y, x):
    """

    Parameters
    ----------
    y :
        
    x :
        

    Returns
    -------

    """
    import matplotlib.style as style
    # Sizing the plot.
    style.use('fivethirtyeight')
    plt.subplots(figsize=(12, 8))
    # Plotting target variable with predictor variable(OverallQual)
    sns.scatterplot(y=y, x=x)
