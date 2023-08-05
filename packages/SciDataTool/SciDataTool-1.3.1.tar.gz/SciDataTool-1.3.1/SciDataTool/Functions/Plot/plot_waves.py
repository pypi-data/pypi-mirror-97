# -*- coding: utf-8 -*-

from itertools import repeat

import matplotlib.pyplot as plt
from numpy import (
    argmin,
    abs,
    squeeze,
    split,
    ndarray,
    cumsum,
    zeros,
    shape,
    concatenate,
    linspace,
    pi,
    cos,
    sin,
    real,
    exp,
    ones_like,
)

from glob import glob
from os import remove
from os.path import join

import imageio
from pyleecan.definitions import config_dict

# Import values from config dict
FONT_NAME = config_dict["PLOT"]["FONT_NAME"]
FONT_SIZE_TITLE = config_dict["PLOT"]["FONT_SIZE_TITLE"]
FONT_SIZE_LABEL = config_dict["PLOT"]["FONT_SIZE_LABEL"]
FONT_SIZE_LEGEND = config_dict["PLOT"]["FONT_SIZE_LEGEND"]
COLORS = config_dict["PLOT"]["COLOR_DICT"]["CURVE_COLORS"]


def plot_waves(
    wavenumbers,
    frequencies,
    Zs=48,
    p=4,
    fs=50,
    is_LF=True,
    legend_list=None,
    color_list=COLORS,
    linestyle_list=["-"],
    linewidth_list=[2],
    title="",
    is_disp_title=True,
    win_title=None,
    save_path="./",
    file_name="waves.gif",
    nframe=25,
):
    """Plots a wave graph

    Parameters
    ----------
    wavenumbers : list
        list of wavenumbers
    frequencies : list
        list of frequencies
    Zs : int
        number of slots
    p : int
        number of pole pairs
    is_LF : bool
        the last quantity is lumped forces -> stator + arrows
    legend_list : list
        list of legends
    color_list : list
        list of colors to use for each curve
    linestyle_list : list
        list of line styles to use for each curve
    linewidth_list : list
        list of line width to use for each curve
    title : str
        title of the graph
    is_disp_title : bool
        boolean indicating if the title must be displayed
    win_title : str
        Title of the plot window
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    file_name : str
        name of the gif file
    nframe : int
        number of frames
    """

    # Number of curves on a axe
    ndatas = len(wavenumbers)

    # Expend default argument
    if 1 == len(color_list) < ndatas:
        # Set the same color for all curves
        color_list = list(repeat(color_list[0], ndatas))
    if 1 == len(linewidth_list) < ndatas:
        # Set the same color for all curves
        linewidth_list = list(repeat(linewidth_list[0], ndatas))
    if 1 == len(linestyle_list) < ndatas:
        # Set the same linestyles for all curves
        linestyle_list = list(repeat(linestyle_list[0], ndatas))
    if legend_list is None:
        legend_list = [
            "f = " + str(f) + " [Hz], r = " + str(wavenumbers[i])
            for i, f in enumerate(frequencies)
        ]

    # Plot
    theta = linspace(0, 2 * pi, 42 * Zs, endpoint=False)
    r = 10 + 4 * (ndatas - 1)
    stator_int = [
        r * 1.1 if ((i % 42) > 5 and (i % 42) < 37) else r for i in range(42 * Zs)
    ]
    stator_ext = [r * 1.2 for i in range(42 * Zs)]
    # rotor = [r-0.5 if ((i%252)>10 and (i%252)<242) else r-1 for i in range(42*Zs)]
    theta2 = linspace(0, 2 * pi, Zs, endpoint=False)
    r2 = [r for i in range(Zs)]
    with imageio.get_writer(join(save_path, file_name), mode="I") as writer:
        for t in linspace(0.0, 1.0 / fs, nframe + 1)[:nframe]:
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            for i, r in enumerate(wavenumbers):
                radius = 10 + 4 * i
                if r == 0:
                    amp = 1
                else:
                    amp = 1
                if r == 0 and frequencies[i] == 0:
                    wave = [radius for j in range(42 * Zs)]
                else:
                    wave = radius + amp * cos(2 * pi * frequencies[i] * t + r * theta)
                if i < (ndatas - 1):
                    ax.plot(
                        theta, real(wave), color=color_list[i], label=legend_list[i]
                    )
                elif is_LF:
                    ax.plot(
                        theta,
                        real(wave),
                        color=color_list[i],
                        linestyle="--",
                        label=legend_list[i],
                    )
                else:
                    ax.plot(
                        theta, real(wave), color=color_list[i], label=legend_list[i]
                    )
            if is_LF:
                ax.fill_between(theta, stator_int, stator_ext, color="#E1E1E0")
                # ax.fill_between(theta, 0, rotor, color="#E8E9E8")
                wave2 = 1 * cos(2 * pi * frequencies[-1] * t + wavenumbers[-1] * theta2)
                ax.quiver(
                    theta2,
                    r2,
                    real(wave2) * cos(theta2),
                    real(wave2) * sin(theta2),
                    color=color_list[i],
                    scale_units="x",
                    scale=6,
                    headlength=2,
                    headaxislength=2,
                )

            bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="k", lw=0.5)
            ax.text(
                0, 12, r"$\, x$", ha="center", va="center", size=10, bbox=bbox_props
            )
            ax.text(0, 16, r"$\!=$", ha="center", va="center", size=10, bbox=bbox_props)
            ax.text(0, 20, r"$+$", ha="center", va="center", size=10, bbox=bbox_props)
            ax.text(
                0,
                24,
                r"$\Rightarrow$",
                ha="center",
                va="center",
                size=10,
                bbox=bbox_props,
            )

            if is_disp_title:
                ax.set_title(title)

            plt.tight_layout()
            ax.legend(loc="center", prop={"family": FONT_NAME, "size": 6})
            if is_LF:
                ax.set_rticks([10 + 4 * i for i in range(ndatas - 1)])
            else:
                ax.set_rticks([10 + 4 * i for i in range(ndatas)])
            ax.set_xticks([0, pi / 2, pi, 3 * pi / 2])
            # ax.set_xticks([])
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_ylim([0, 11 + 4 * ndatas])
            ax.spines["polar"].set_visible(False)
            save_path_temp = save_path + "/temp_" + str(t) + ".png"
            fig.savefig(save_path_temp)
            plt.close()
            image = imageio.imread(save_path_temp)
            writer.append_data(image)

    for file in glob(save_path + "/temp_*"):
        remove(file)

    # ax.title.set_fontname(FONT_NAME)
    # ax.title.set_fontsize(FONT_SIZE_TITLE)

    # if win_title:
    #     fig.canvas.set_window_title(win_title)
