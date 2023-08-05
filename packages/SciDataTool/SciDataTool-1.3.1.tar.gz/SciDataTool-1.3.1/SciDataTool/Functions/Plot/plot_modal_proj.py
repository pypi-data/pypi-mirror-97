from numpy import zeros, array, arange, meshgrid, squeeze, abs as np_abs, max as np_max

from ...Functions.Plot.plot_4D import plot_4D


def plot_modal_proj(
    modal_proj,
    mode_labels,
    nat_freqs,
    save_path=None,
    is_show_fig=True,
    label="",
):
    """Plot the result of the modal projection at a given frequency

    Parameters
    ----------
    modal_cont : dict
        result of the modal contribution
    mode_labels : list
        list of mode labels
    nat_freqs : list
        list of natural frequencies
    save_path : str
        location to store the figure
    is_show_fig : bool
        True to call show at the end of the plot
    label : str
        name of the FRF
    """

    title = "Modal projection of " + label

    nloads = len(modal_proj)
    nmodes = len(mode_labels)
    Zdatas = zeros((nloads, nmodes))
    annot = zeros((nloads, nmodes), dtype=int)
    yticklabels = []
    size = zeros((nloads, nmodes))
    i = 0
    for key in modal_proj.keys():
        Zdatas[i, :] = squeeze(np_abs(array(modal_proj[key])))
        yticklabels.append(key)
        size[i, :] = 1000 * Zdatas[i, :] / np_max(Zdatas[i, :])
        annot[i, :] = (array(nat_freqs)).astype(int)
        i += 1
    x = arange(nmodes)
    y = arange(nloads)
    x_map, y_map = meshgrid(x, y)
    x_flat = x_map.flatten()
    y_flat = y_map.flatten()
    Zdata_flat = Zdatas.flatten()
    size_flat = size.flatten()
    zmax = max(Zdata_flat)
    annotations = annot.flatten()

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
        xlabel="Modes",
        ylabel="Loadcases",
        zlabel=label,
        annotations=annotations,
        type="scatter",
        title=title,
        save_path=save_path,
        is_show_fig=is_show_fig,
    )
