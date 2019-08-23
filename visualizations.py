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


def overlapping_density(data, package='sns', input_cat='Role', target_vars='Salary'):
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
    input_vars = set(list(data[input_cat]))

    # Set size of figure
    fig,axes = plt.subplots(figsize=(16, 10), dpi=80)

    if package == "sns":
        for variable in input_vars:
            sns.kdeplot(data[target_vars], hue=input_vars)
       
    elif package == 'matplotlib':
        for variable in input_vars:
            plt.hist(clean[target_vars], density=True, label=variable, figure = fig)

    return fig


def distribution_timeseries(data, input_vars='Role', target_vars='Salary'):
    """ Function that returns a Seaborn timeseries of target_variable, subset by categories"""
    fig = plt.figure(figsize = (12,10))
    
    ax = sns.lineplot(x="Year", y=target_vars, data=data, hue=input_vars)
    plt.ylabel('Salary (K)')
    plt.xlabel('Year')
    
    locs,labels = plt.yticks()
    ticks = ax.get_yticks()
    plt.yticks(locs, ticks/1000)
    
    plt.title('H1B '+target_vars+' Information by '+input_vars)
    plt.legend(ncol = 3, fontsize = 11, loc='upper center')
    
    return fig

def boxplot_plot(data, package='sns', input_cat='Role', target_vars='Salary'):
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
  input_vars = set(list(data[input_cat]))

    # Set size of figure
    fig = plt.figure(figsize=(16, 10), dpi=80)

    if package == "sns":
        for variable in input_vars:
            sns.boxplot(data[target_vars], hue=input_vars)

       
    elif package == 'matplotlib': # apparently want a line plot here?
        for variable in input_vars:
            plt.box(data[data[input_vars]==variable][target_vars], label=variable, linewidth=None, color=None, figure = fig)

    return fig


def visualization_one(data, target_var = 'Salary', input_vars= 'Role', output_image_name='Salary_by_Role'):
    """
    The visualization functions are what is used to create each individual image.
    The function should be repeatable if not generalizable
    The function will call either the boxplot or density plot functions you wrote above

    :param target_var:
    :param input_vars:
    :param output_image_name: the desired name for the image saved
    :return: outputs a saved png file and returns a fig object for testing
    """
    overlapping_density
                          

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