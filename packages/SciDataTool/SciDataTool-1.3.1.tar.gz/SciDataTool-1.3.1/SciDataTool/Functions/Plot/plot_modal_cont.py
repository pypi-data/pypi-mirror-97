# -*- coding: utf-8 -*-

from numpy import zeros, array, arange, meshgrid, abs as np_abs, max as np_max

from ...Functions.Plot.plot_4D import plot_4D


def plot_modal_cont(
    modal_cont,
    mode_labels,
    nat_freqs,
    ifrq,
    freq=None,
    save_path=None,
    is_show_fig=True,
    label="",
):
    """Plot the result of the modal contribution at a given frequency

    Parameters
    ----------
    modal_cont : dict
        result of the modal contribution
    mode_labels : list
        list of mode labels
    nat_freqs : list
        list of natural frequencies
    ifrq : int
        index of freq to use for the plot
    freq : float
        requested frequency
    save_path : str
        location to store the figure
    is_show_fig : bool
        True to call show at the end of the plot
    label : str
        name of the FRF
    """
    modal_cont_ext = modal_cont["expansion_ext"]
    nmodes = len(mode_labels)
    nloads = len(list(modal_cont_ext.keys()))
    zmax = 0
    Zdatas = zeros((nloads, nmodes))
    annot = zeros((nloads, nmodes), dtype=int)

    if freq is not None:
        # single frequency
        title = "Modal contribution of " + label + " at " + str(freq) + " Hz"
    else:
        title = "Modal contribution of " + label

    i_lc = 0
    yticklabels = list()
    for lc in modal_cont_ext.keys():
        modal_cont_lc = array(modal_cont_ext[lc])
        modal_cont_ind = [int(x) for x in array(modal_cont_ext[lc])[:, 0].tolist()]
        Zdatas[i_lc, modal_cont_ind] = np_abs(modal_cont_lc[:, ifrq + 1])
        yticklabels.append(lc)
        annot[i_lc, modal_cont_ind] = (array(nat_freqs)[modal_cont_ind]).astype(int)
        i_lc += 1

    x = arange(nmodes)
    y = arange(nloads)
    x_map, y_map = meshgrid(x, y)
    x_flat = x_map.flatten()
    y_flat = y_map.flatten()
    zmax = np_max(Zdatas)
    annotations = annot.flatten()

    size = 1000 * Zdatas / zmax
    Zdata_flat = Zdatas.flatten()
    size_flat = size.flatten()

    xticklabels = mode_labels

    plot_4D(
        x_flat,
        y_flat,
        Zdata_flat,
        size_flat,
        z_max=zmax,
        z_min=0,
        xticks=x,
        yticks=y,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        xlabel="Mode",
        ylabel="Loadcase",
        zlabel=label,
        annotations=annotations,
        title=title,
        type="scatter",
        save_path=save_path,
        is_show_fig=is_show_fig,
    )
