import os
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def setup_fonts(plt, data):
    font_properties = data['plot_config']['font']

    plt.rcParams.update({
    "text.usetex": True,     # use inline math for tikz
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    "font.family": font_properties['font_family'],
    "pgf.preamble": "\n".join([
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{"+font_properties['tex_package']+"}"
        ])
    })

def calculate_inch_fig_size(width_mm, height_mm):
    return (width_mm * 0.03937007874, height_mm * 0.03937007874)

def remove_upper_axis(ax):
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

def remove_right_axis(ax):
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')

def label_alignment(rotation : str):
    if rotation=='horizontal': 
        return 'top'
    return 'bottom'

def get_fontsize(data):
    fontsize_pt = data['plot_config']['font']['fontsize_pt']
    return fontsize_pt

def scaleRGB(rgb_list):
    return (rgb_list[0] * 1.0/255.0, rgb_list[1] * 1.0/255.0, rgb_list[2] * 1.0/255.0)

def set_labels(fig, ax, data, pad): 
    '''
    Sets fontsize (pt), labels and their rotation.
    The labels are placed at each end of the axes so that we don't waste too much space.
    The correct label position will be calculated automatically.
    Currently the user needs to find suitable ticks, so that labels and ticks don't overlap!
    '''
    axis_labels = data['axis_labels']
    ax.set_xlabel(axis_labels['x']['text'], fontsize=get_fontsize(data), ha="right", 
                  va=label_alignment(axis_labels['x']['rotation']), rotation=axis_labels['x']['rotation'])
    ax.set_ylabel(axis_labels['y']['text'], fontsize=get_fontsize(data), ha="right", 
                  va=label_alignment(axis_labels['y']['rotation']), rotation=axis_labels['y']['rotation'])

    # compute axis size in points
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width * 72, bbox.height * 72

    # compute relative padding
    lwX = ax.spines['bottom'].get_linewidth()
    # TODO if use_scientific_notations is True, then take ~70% of fontsize * ~1/4 and add it to the padding

    lwY = 0 #ax.spines['left'].get_linewidth()

    # coordinates in percentage of the figure main body size!
    ax.xaxis.set_label_coords(1, -(pad - lwX) / height)

    # coordinates in percentage of the figure main body size!
    ax.yaxis.set_label_coords(-(pad - lwY) / width, 1)

def mplot_color(rgb_list):
    r,g,b = rgb_list[0] / 255., rgb_list[1] / 255., rgb_list[2] / 255.
    return (r,g,b)

def plot_lines(ax, data): #error_path, methods, linewidth_pt, has_xscale_log=True, has_yscale_log=True
    i = 0
    for d in data['data']:
        linewidth = data['plot_config']['plot_linewidth_pt']
        color = mplot_color(data['plot_color'][i])
        ax.plot(d[0], d[1], linewidth=linewidth, color=color) 
        i += 1

def _apply_axis_range(ax, axis, data):
    try:
        axis_range = data['axis_properties'][axis]['range'][0], data['axis_properties'][axis]['range'][1]
    except:
        axis_range = None

    if axis_range is not None:
        if axis == 'x':
            ax.set_xlim(axis_range)
        else:
            ax.set_ylim(axis_range)

def _apply_x_axes_properties(fig, ax, data):
    '''
    Because matplotlib has different function names for each axes, we also need two functions for the two axes.
    '''
    try:
        props = data['axis_properties']['x']
    except:
        return

    if props['use_log_scale']:
        ax.set_xscale('log')

    if props['ticks'] is not None:
        ax.set_xticks(props['ticks'])
        if not props['use_scientific_notations']: # can only apply if we have specific ticks
            ax.set_xticklabels(props['ticks'])
    
    ax.xaxis.set_minor_formatter(FormatStrFormatter(""))

def _apply_y_axes_properties(fig, ax, data):
    '''
    Because matplotlib has different function names for each axes, we also need two functions for the two axes.
    '''
    try:
        props = data['axis_properties']['y']
    except:
        return

    if props['use_log_scale']:
        ax.set_yscale('log')

    if props['ticks'] is not None:
        ax.set_yticks(props['ticks'])
        if not props['use_scientific_notations']: # can only apply if we have specific ticks
            ax.set_yticklabels(props['ticks'])
    
    ax.yaxis.set_minor_formatter(FormatStrFormatter(""))

def apply_axes_properties_and_labels(fig, ax, data):
    _apply_axis_range(ax, 'x', data)
    _apply_axis_range(ax, 'y', data)

    if not data['plot_config']['has_right_axis']: 
        remove_right_axis(ax)
    if not data['plot_config']['has_upper_axis']: 
        remove_upper_axis(ax)

    tick_lw_pt = data['plot_config']['tick_linewidth_pt']
    plt.tick_params(width=tick_lw_pt, length=(tick_lw_pt * 4), labelsize=get_fontsize(data), pad=(tick_lw_pt * 2))
    set_labels(fig, ax, data, pad=(tick_lw_pt * 6))
    # if use_scientific_notations True, displaystyle is used in pgf --> offset of ticks changes 

    _apply_x_axes_properties(fig, ax, data)
    _apply_y_axes_properties(fig, ax, data)


def place_marker(ax, marker_data):
    try:
        vlines = marker_data['vertical_lines']
    except:
        vlines = []

    for vl in vlines:
        ax.axvline(x=vl['pos'], color=scaleRGB(vl['color']), linewidth=vl['linewidth_pt'], linestyle=vl['linestyle'])

    try:
        hlines = marker_data['horizontal_lines']
    except:
        hlines = []

    for hl in hlines:
        ax.axhline(y=hl['pos'], color=scaleRGB(hl['color']), linewidth=hl['linewidth_pt'], linestyle=hl['linestyle'])

def generate(module_data, to_path, pdf_filename):
    setup_fonts(plt, module_data) 
    figsize = calculate_inch_fig_size(module_data['total_width'], module_data['total_height'])
    #constrained_layout: https://matplotlib.org/3.2.1/tutorials/intermediate/constrainedlayout_guide.html
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    fig.set_constrained_layout_pads(w_pad=0, h_pad=0,
        hspace=0., wspace=0.)

    plot_lines(ax, module_data)
    
    apply_axes_properties_and_labels(fig, ax, module_data)
    
    grid_properties = module_data['plot_config']['grid']
    plt.grid(color=scaleRGB(grid_properties['color']), linestyle=grid_properties['linestyle'], linewidth=grid_properties['linewidth_pt'])

    place_marker(ax, module_data['markers'])

    path = os.path.join(to_path, pdf_filename).replace('\\','/')
    plt.savefig(path, pad_inches=0.0, dpi=500)