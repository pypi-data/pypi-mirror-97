from numpy import transpose, concatenate, nan, max as np_max

from ...Functions.Plot.plot_2D import plot_2D
from ...definitions import config_dict

# Get default colors, fonts and linestyles
COLOR_DICT = config_dict["PLOT"]["COLOR_DICT"]["CURVE_COLORS"]
FONT_NAME = config_dict["PLOT"]["FONT_NAME"]
LINE_STYLE = config_dict["PLOT"]["LINE_STYLE"]


def plot_order_analysis(
    speeds,
    A_overall,
    A_orders,
    legend_list,
    db_min=10,
    db_max=100,
    save_path=None,
    xlabel="Rotation speed [rpm]",
    ylabel="Acoustic power [dBA]",
    title="Order tracking analysis",
    is_disp_title=True,
    is_grid=True,
    is_show_fig=True,
    fig=None,
    ax=None,
    is_db=True,
):
    """
    Plot spectrogram from a variable speed simulation

    speeds: ndarray
        Array of speed values
    freqs : ndarray
        Array of frequency vectors for each speed
    A_overall : ndarray
        maximum level function of speed
    A_orders : ndarray
        Amplitude array per speed and order
    legend_list : list
        Legend for each order
    db_min : float
        lines under db_min are not displayed
    db_max : float
        maximum dB scale
    save_path : str
        location to store the figure
    xlabel : str
        label for the x-axis
    ylabel : str
        label for the y-axis
    title : str
        title of the graph
    is_disp_title : bool
        boolean indicating if the title must be displayed
    is_grid : bool
        boolean indicating if the grid must be displayed
    is_show_fig : bool
        True to call show at the end of the plot
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data

    Returns
    -------
        ax : axes

    Raises
    ------
    PlotError
    """

    # Number of orders
    Norders = A_orders.shape[1]

    # Build the color and linestyle lists
    # Copy default COLOR_DICT
    color_list = COLOR_DICT.copy()
    # Duplicate first line style Ncolor times
    ii = 0
    linestyle_list = [LINE_STYLE[ii] for color in COLOR_DICT]

    # Append color and linestyle lists while there are less colors than curves to plot
    while len(color_list) < Norders:
        color_list.extend(COLOR_DICT.copy())
        ii = ii + 1
        linestyle_list.extend([LINE_STYLE[ii] for color in COLOR_DICT])

    # Concatenate orders amplitude and overall value
    Ydatas = concatenate((A_overall[:, None], A_orders), axis=1)

    # Append black color to the color and line_style list
    colors = ["#000000"] + color_list
    linestyles = [LINE_STYLE[0]] + linestyle_list
    legends = ["Overall"] + legend_list

    # Put zeros to NaN so they are not plotted
    Ydatas[Ydatas == 0] = nan

    # Set maximum value on y-axis
    if is_db:
        y_min = db_min
        y_max = 1.05 * np_max(A_overall)
    else:
        y_min = None
        y_max = None

    # Plot 2D
    ax = plot_2D(
        transpose(speeds),
        transpose(Ydatas),
        legend_list=legends,
        color_list=colors[0 : Norders + 1],
        linestyle_list=linestyles[0 : Norders + 1],
        save_path=save_path,
        y_min=y_min,
        y_max=y_max,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        is_disp_title=is_disp_title,
        is_show_fig=is_show_fig,
        fig=fig,
        ax=ax,
    )

    return ax
