import matplotlib.pyplot as plt
from numpy import vstack, linspace, max as np_max

from ...Functions.init_fig import init_subplot, init_fig
from ...definitions import config_dict

COLORMAP = config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"]
FONT_NAME = config_dict["PLOT"]["FONT_NAME"]
FONT_SIZE_TITLE = config_dict["PLOT"]["FONT_SIZE_TITLE"]
FONT_SIZE_LABEL = config_dict["PLOT"]["FONT_SIZE_LABEL"]
FONT_SIZE_LEGEND = config_dict["PLOT"]["FONT_SIZE_LEGEND"]


def plot_spectrogram(
    speeds,
    freqs,
    A_orders,
    freq_max=10000,
    order_width=15,
    db_min=0,
    db_max=None,
    save_path=None,
    Norders=100,
    zlabel=None,
    title=None,
    is_disp_title=True,
    type_spectro=0,
    is_reverse_spectro=False,
    speed_max=None,
    is_show_fig=None,
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
    A_orders : ndarray
        Amplitude array per speeds and orders(Nspeeds, Norders)
    freq_max : float
        maximum frequency
    order_width : float
        width of the order lines
    db_min : float
        lines under db_min are not displayed
    db_max : float
        maximum dB scale
    save_path : str
        location to store the figure
    Norders : integer
        number of orders
    xlabel : str
        label for the x-axis
    ylabel : str
        label for the y-axis
    zlabel : str
        label for the z-axis
    title : str
        title of the graph
    is_disp_title : bool
        boolean indicating if the title must be displayed
    type_spectro : int
        type of spectrogram (0: per order, 1: per speed)
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data

    Returns
    -------

    Raises
    ------
    PlotError
    """

    # Create figure if needed
    if fig is None and ax is None:
        fig, ax = init_subplot(fig=None)

    colorbar = None

    # Number of orders to plot
    Norders = min([Norders, freqs.shape[1]])

    if is_db:
        if db_max is None:
            db_max = int(1.05 * np_max(A_orders.flatten("C")))

    if is_reverse_spectro:
        xlabel = "Rotation speed [rpm]"
        ylabel = "Frequency [Hz]"
    else:
        xlabel = "Frequency [Hz]"
        ylabel = "Rotation speed [rpm]"

    if type_spectro == 0:  # plot order per order
        # Duplicate speed vector to plot a pcolormesh
        if is_reverse_spectro:
            xx = vstack((speeds, speeds))
        else:
            yy = vstack((speeds, speeds))

        # Loop on orders
        for k in range(Norders):
            if is_reverse_spectro:
                y = freqs[:, k]
                yy = vstack((y - order_width, y + order_width))
            else:
                x = freqs[:, k]
                xx = vstack((x - order_width, x + order_width))
            c = A_orders[:, k]
            cc = vstack((c, c))
            if np_max(c) > db_min:
                colorbar = ax.pcolormesh(
                    xx,
                    yy,
                    cc,
                    cmap=COLORMAP,
                    vmin=db_min,
                    vmax=db_max,
                    shading="gouraud",
                )
    elif type_spectro == 1:  # plot speed by speed  #TODO

        print("type_spectro==1 not available yet")

        pass
        # for i in range(len(freqs)):
        #     c = ax.scatter(
        #         freqs[i],
        #         speeds,
        #         c=A_orders[i],
        #         vmin=db_min,
        #         vmax=db_max,
        #         marker="s",
        #         cmap=COLORMAP,
        #     )

    if is_db:
        v = linspace(db_min, db_max, int((db_max - db_min) / 10) + 1, endpoint=True)
        if colorbar is not None:
            clb = fig.colorbar(colorbar, ticks=v, format="%.4g")
    else:
        if colorbar is not None:
            clb = fig.colorbar(colorbar, format="%.4g")
    if colorbar is not None:
        clb.ax.set_title(zlabel, fontsize=FONT_SIZE_LEGEND, fontname=FONT_NAME)
        clb.ax.tick_params(labelsize=FONT_SIZE_LEGEND)

        for l in clb.ax.yaxis.get_ticklabels():
            l.set_family(FONT_NAME)
    if is_reverse_spectro:
        ax.set_ylim([0, freq_max])
        if speed_max is not None:
            ax.set_xlim([0, speed_max])
    else:
        ax.set_xlim([0, freq_max])
        if speed_max is not None:
            ax.set_ylim([0, speed_max])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if is_disp_title:
        ax.set_title(title)

    for item in (
        [ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()
    ):
        item.set_fontname(FONT_NAME)
        item.set_fontsize(FONT_SIZE_LABEL)
    ax.title.set_fontname(FONT_NAME)
    ax.title.set_fontsize(FONT_SIZE_TITLE)

    if save_path is not None:
        fig.savefig(save_path)
        plt.close()

    if is_show_fig:
        fig.show()
