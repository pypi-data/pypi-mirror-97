import tempfile
import os
import copy

from .tex import make_tex, calculate
from .slide_pptx import make_pptx
from .html import make_html
from . import default_layouts
from .element_data import Image, Plot

class Error(Exception):
    def __init__(self, message):
        self.message = message

backends = {
    "tikz": make_tex,
    "pptx": make_pptx,
    "html": make_html
}

# ------- dictionary: overwrite, replace, merge & algin --------
def overwrite(name: list, val, layout: dict):
    if len(name) == 1:
        layout[name[0]] = val
        return
    overwrite(name[1:], val, layout[name[0]])

def replace_option(name: str, val, layout: dict):
    # first.second.third -> [ first, second, third ]
    path = name.split(sep='.')
    overwrite(path, val, layout)

def modify_default_layout(user: dict, type='grid'):
    default = copy.deepcopy(default_layouts.layouts[type])

    for key,val in user.items():
        replace_option(key, val, default)

    return default

def merge_data_into_layout(data, layout):
    # layout['type'] = data['type']
    directions = ["north", "south", "east", "west"]

    num_rows = len(data["elements"])
    num_cols = len(data["elements"][0])
    layout['num_rows'] = num_rows
    layout['num_columns'] = num_cols

    # initialize empty matrix for elements
    layout["elements_content"] = [[{} for i in range(num_cols)] for i in range (num_rows)]

    for row in range(num_rows):
        for col in range(num_cols):
            elem = layout["elements_content"][row][col]
            data_elem = data["elements"][row][col]

            try:
                elem["label"] = data_elem["label"]
            except KeyError:
                pass

            # copy captions, if set
            elem["captions"] = {}
            for d in directions:
                try:
                    caption = data_elem["captions"][d]
                except:
                    caption = ""
                elem["captions"][d] = caption

            # add frame from user (optional, default: no frame)
            try:
                frame = data_elem["frame"]
            except: # do not set the frame
                frame = None
            if frame is not None: elem["frame"] = frame

            # add crop marker (optional, default: no marker)
            try:
                marker = data_elem["crop_marker"]
            except: # do not set marker
                marker = None
            if marker is not None: elem["marker"] = marker

            # add lines (optional, default: no lines)
            try:
                lines = data_elem["lines"]
            except: # do not set lines
                lines = None
            if lines is not None: elem["lines"] = lines

            # add the image data itself (raw): matrix of rgb
            # assert ((data_elem["image"]).shape[2] == 3)
            try:
                elem["image"] = data_elem["image"]
            except KeyError:
                raise Error('An element (row: '+str(row)+', column: '+str(col)+') of one of your grids has no set image!')

    # add column_titles
    for d in ['north', 'south']:
        # change text color
        try:
            layout["column_titles"][d]["text_color"] = data["column_titles"][d]["text_color"]
        except: # keep default
            pass

        # change background color of column text field
        try:
            layout["column_titles"][d]["background_colors"] = data["column_titles"][d]["background_colors"]
        except: # keep default: [0,0,0]
            pass

        # add content
        try:
            layout["column_titles"][d]["content"] = data["column_titles"][d]["content"]
        except: # set default: list of empty strings
            layout["column_titles"][d]["content"] = [""] * num_cols

    # add row_titles
    for d in ['east', 'west']:
        # change text color
        try:
            layout["row_titles"][d]["text_color"] = data["row_titles"][d]["text_color"]
        except: # keep default
            pass

        # change background color of column text field
        try:
            layout["row_titles"][d]["background_colors"] = data["row_titles"][d]["background_colors"]
        except: # keep default: [0,0,0]
            pass

        # add text-based content
        try:
            layout["row_titles"][d]["content"] = data["row_titles"][d]["content"]
        except: # set default: list of empty strings
            layout["row_titles"][d]["content"] = [""] * num_rows

    # titles
    for d in directions:
        # add text-based content
        try:
            layout['titles'][d]['content'] = data['titles'][d]
        except: # set default: empty string
            layout['titles'][d]['content'] = ''

    # set image size (ratio), preferably in correct unit (px) if possible
    img = layout["elements_content"][0][0]["image"]
    layout["img_width_px"] = 1
    layout["img_height_px"] = img.aspect_ratio
    if isinstance(img, Image) and img.width_px is not None:
        layout["img_width_px"] = img.width_px
        layout["img_height_px"] = img.height_px

    return layout

def merge(modules: dict, layouts: dict):
    merged_dicts = []
    for i in range(len(modules)):
        merged_dicts.append(merge_data_into_layout(modules[i], layouts[i]))
    return merged_dicts

def align_modules(modules, width):
    num_modules = len(modules)
    assert(num_modules!=0)

    if num_modules == 1:
        modules[0]["total_width"] = width
        calculate.resize_to_match_total_width(modules[0])
        modules[0]['total_height'] = calculate.get_total_height(modules[0])

    sum_inverse_aspect_ratios = 0
    inverse_aspect_ratios = []
    for m in modules:
        image_aspect_ratio = m['img_height_px'] / float(m['img_width_px'])
        a = m['num_rows'] / float(m['num_columns']) * image_aspect_ratio

        sum_inverse_aspect_ratios += 1/a
        inverse_aspect_ratios.append(1/a)

    sum_fixed_deltas = 0
    i = 0
    for m in modules:
        w_fix = calculate.get_min_width(m)
        h_fix = calculate.get_min_height(m)

        sum_fixed_deltas += w_fix - h_fix * inverse_aspect_ratios[i]
        i += 1

    height = (width - sum_fixed_deltas) / sum_inverse_aspect_ratios

    for m in modules:
        m['total_height'] = height
        calculate.resize_to_match_total_height(m)
        m['total_width'] = calculate.get_total_width(m)

def get_backend(filename):
    # Select the correct backend based on the filename
    extension = os.path.splitext(filename)[1].lower()
    if extension == ".pptx":
        backend = 'pptx'
    elif extension == ".html":
        backend = 'html'
    elif extension == ".pdf":
        backend = 'tikz'
    else:
        raise ValueError(f"Could not derive backend from filename '{filename}'")
    return backend

def align_horizontal_modules(modules, width_cm):
    layouts = []
    for m in modules:
        layouts.append(modify_default_layout(m.data['layout']))

    modules_data_list = [m.data for m in modules]
    merged_data = merge(modules_data_list, layouts)
    align_modules(merged_data, width_cm*10.)
    return merged_data

def make_image_tmp_dir(intermediate_dir):
    # Create temporary folder for images, generated .tex files, LaTeX output, etc
    # Unless the user specified a folder for those files
    if intermediate_dir is not None and os.path.isdir(intermediate_dir):
        temp_folder = None
        temp_dir = os.path.abspath(intermediate_dir)
    else:
        temp_folder = tempfile.TemporaryDirectory()
        temp_dir = temp_folder.name

    return temp_dir, temp_folder


def figure(modules, width_cm, filename, intermediate_dir, tex_packages):
    """
    Grid rows: Creates a figure by putting grids next to each other, from left to right.
    Grid columns: stacks rows vertically.
    Aligns the height of the given grids such that they fit the given total width.

    args:
        grids: a list of lists of Grids (figuregen.Grid), which stacks horizontal figures vertically
        width_cm: total width of the figure in centimeters
        intermediate_dir: folder to write .tex and other intermediate files to. If set to None, uses a temporary one.
        tex_packages: a list of strings. Valid packages looks like ['{comment}', '[T1]{fontenc}'] without the prefix '\\usepackage'.
    """
    backend = get_backend(filename)

    merged_data = []
    for fig_idx in range(len(modules)):
        merged_data.append(align_horizontal_modules(modules[fig_idx], width_cm))

    temp_dir, temp_folder = make_image_tmp_dir(intermediate_dir)

    from concurrent.futures import ThreadPoolExecutor
    generated_data = []
    with ThreadPoolExecutor() as executor:
        # Launch futures for each module
        for fig_idx in range(len(modules)):
            generated_data.append([])
            for mod_idx in range(len(modules[fig_idx])):
                module = merged_data[fig_idx][mod_idx]
                future = executor.submit(backends[backend].generate, module, figure_idx=fig_idx,
                    module_idx=mod_idx, temp_folder=temp_dir, tex_packages=tex_packages)
                generated_data[fig_idx].append(future)

        # Replace all futures by their results
        for fig_idx in range(len(modules)):
            for mod_idx in range(len(modules[fig_idx])):
                generated_data[fig_idx][mod_idx] = generated_data[fig_idx][mod_idx].result()

    backends[backend].combine(generated_data, filename, temp_folder=temp_dir)

    if temp_folder is not None:
        temp_folder.cleanup()


def horizontal_figure(modules, width_cm: float, filename, intermediate_dir, tex_packages):
    """
    Creates a figure by putting grids next to each other, from left to right.
    Aligns the height of the given grids such that they fit the given total width.

    Args:
        grids: a list of Grids (figuregen.Grid)
        width_cm: total width of the figure in centimeters
        intermediate_dir: folder to write .tex and other intermediate files to. If set to None, uses a temporary one.
        tex_packages: a list of strings. Valid packages looks like ['{comment}', '[T1]{fontenc}'] without the prefix '\\usepackage'.
    """
    backend = get_backend(filename)
    merged_data = align_horizontal_modules(modules, width_cm)
    temp_dir, temp_folder = make_image_tmp_dir(intermediate_dir)

    generated_data = []
    for i in range(len(modules)):
        module = merged_data[i]
        generated_data.append(backends[backend].generate(module,
                                                        figure_idx=0, module_idx=i,
                                                        temp_folder=temp_dir, tex_packages=tex_packages))

    backends[backend].combine([generated_data], filename, temp_folder=temp_dir)

    if temp_folder is not None:
        temp_folder.cleanup()