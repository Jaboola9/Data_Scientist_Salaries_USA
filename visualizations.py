"""
This module is for your final visualization code
One visualization per hypothesis question is required
A framework for each type of visualization is provided
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set specific parameters for the visualizations
large = 22
med = 16
small = 12
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


def overlapping_density(data, input_cat='role', target_vars='salary',
                        package='sns'):
    """
    Function takes package name, input variables, and target variable as input.
    Returns a figure with overlaping density plots on a single set of axes.
    """
    input_vars = list(set(data[input_cat]))

    # Set size of figure
    fig, axes = plt.subplots(figsize=(16, 10), dpi=80)

    if package == "sns":
        for variable in input_vars:
            sns.kdeplot(data[data[input_cat] == variable][target_vars],
                        label=variable, figure=fig)

    elif package == 'matplotlib':
        for variable in input_vars:
            plt.hist(data[data[input_cat] == variable][target_vars],
                     density=True, label=variable, figure=fig)

    plt.title('H1B '+target_vars.title()+' Distribution by '
              + input_vars.title())
    plt.xlabel(target_vars.title())
    plt.ylabel('Density')
    plt.legend(fontsize=10)

    return fig


def distribution_timeseries(data, time_cat='year', input_cats='role',
                            target_vars='salary'):
    """Function that returns timeseries of target_variable, by categories"""
    input_vars = list(set(data[input_cat]))

    fig = plt.figure(figsize=(12, 10), dpi=80)
    for variable in input_vars:
        sns.lineplot(x=time_cat, y=target_vars, data=data, hue=input_cat,
                     figure=fig)

    if target_vars == 'salary':
        locs, labels = plt.yticks()
        ticks = ax.get_yticks()
        plt.yticks(locs, ticks/1000)
        plt.ylabel('Salary (K)')
    else:
        plt.ylabel(target_vars.title())

    plt.xlabel(input_cats.title())
    plt.title('H1B '+target_vars.title()+' Information by '+input_vars.title())
    plt.legend(ncol=3, fontsize=11)

    return fig


def boxplot_plot(data, grouping='year', input_cat='role', target_vars='salary',
                 package='sns'):
    """ Same specifications and requirements as overlapping density plot."""

    input_vars = set(data[input_cat])

    # Set size of figure
    fig = plt.figure(figsize=(16, 10), dpi=80)

    if package == "sns":
        ax = sns.boxplot(x=grouping, y=target_vars, hue=input_cat, data=data)
    elif package == 'matplotlib':
        for variable in input_vars:
            plt.box(data[data[input_vars] == variable][target_vars],
                    label=variable, linewidth=None, color=None, figure=fig)
    plt.legend(fontsize=11)
    plt.ylabel(target_vars.title())
    plt.xlabel(grouping.title())

    if ((grouping == 'role') | (grouping == 'region') |
    (grouping == 'industry')):
        for item in ax.get_xticklabels():
            item.set_rotation(45)
            plt.xlabel(grouping.title(), fontsize=8)

    plt.title(target_vars.title()+' by '+input_cat.title()+', grouped by '
              + grouping.title())
    return fig


def visualization_one(data, output_image_name='Salary_Distribution_by_Role'):
    """
    :param target_var:
    :param input_vars:
    :param output_image_name: the desired name for the image saved
    :return: outputs a saved png file and returns a fig object for testing
    """

    fig = overlapping_density(data, input_cat='role', target_vars='salary')

    plt.xlabel(target_vars.title(), figure=fig)
    plt.ylabel('Density', figure=fig)
#     plt.title(target_vars.title()+' Distribution by '+input_vars.title(), figure=fig)
    plt.legend(fontsize=10)
    plt.show()

    # exporting the image to the img folder
    plt.savefig(f'img/{output_image_name}.png', transparent=True,
                figure=fig)
    return fig


def visualization_two(data, target_var='salary', input_vars='region',
                      output_image_name='Salary_by_Region'):
    fig = overlapping_density(data, input_cat=input_vars,
                              target_vars=target_var)
    plt.savefig(f'img/{output_image_name}.png', transparent=True,
                figure=fig)

    return fig


def visualization_three(output_image_name):
    fig = distribution_timeseries(data)
    return fig


def visualization_four(output_image_name):
    pass
