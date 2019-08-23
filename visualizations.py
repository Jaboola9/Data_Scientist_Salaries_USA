"""
This module is for your final visualization code.
One visualization per hypothesis question is required.
A framework for each type of visualization is provided.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set specific parameters for the visualizations
large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def overlapping_density(package='sns', input_vars=['Role'], target_vars='Salary'):
    """
    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure with overlaping density plots on a single set of axes.

    Should be able to call this function in later visualization code.

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw an error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """

    # Set size of figure
    fig,axes = plt.subplots(figsize=(16, 10), dpi=80, nrow=nrow)

    # Starter code for figuring out which package to use
    if package == "sns":
        for variable in input_vars:
            sns.kdeplot(clean[target_vars], hue=input_vars)
       
    elif package == 'matplotlib':
        for variable in input_vars:
            plt.plot(clean[target_vars], label=None, linewidth=None, color=None, figure = fig)

    return fig


def boxplot_plot(package='sns', input_vars=['Role'], target_vars='Salary'):
    """
    Same specifications and requirements as overlapping density plot

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """
    # Set size of figure
    fig,axes = plt.subplots(figsize=(16, 10), dpi=80, nrow=nrow)
    
    # Starter code for figuring out which package to use
    if package == "sns":
        for variable in input_vars:
            sns.boxplot(clean[target_vars], hue=input_vars, ax=axes[nr])
       
    elif package == 'matplotlib': # apparently want a line plot here?
        for variable in input_vars:
            plt.box(clean[clean[variable][target_vars], label=variable, linewidth=None, color=None, figure = fig, kind='hist')

    return fig


def visualization_one(target_var = None, input_vars= None, output_image_name=None):
    """
    The visualization functions are what is used to create each individual image.
    The function should be repeatable if not generalizable
    The function will call either the boxplot or density plot functions you wrote above

    :param target_var:
    :param input_vars:
    :param output_image_name: the desired name for the image saved
    :return: outputs a saved png file and returns a fig object for testing
    """
    ###
    # Main chunk of code here
    # Call either box plot or density for each of these viz
    ###

    # Starter code for labeling the image
    plt.xlabel(None, figure = fig)
    plt.ylabel(None, figure = fig)
    plt.title(None, figure= fig)
    plt.legend()

    # exporting the image to the img folder
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)
    return fig


# please fully flesh out this function to meet same specifications of visualization one

def visualization_two(output_image_name):
    pass

def visualization_three(output_image_name):
    pass

def visualization_four(output_image_name):
    pass