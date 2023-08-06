import os
import threading
from . import html_element #, html_plot, chartjs # NOTE: currently chartjs is not used
from ..element_data import *

'''
in HTML format we
 - ignore background colors for whole figure (for now), the background color is white
 - do not support 'dashed' markers - if a marker is 'dashed' the marker will be normal (but still has a marker)
 - only support text rotation by 0° and +-90°
'''

class GridError(Exception):
    def __init__(self, row, col, message):
        self.message = f"Error in row {row}, column {col}: {message}"

def html_header_and_styles():
    header_lines = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',

        #'<script src="./scripts/Chart.min.js"></script>', # NOTE: currently chartjs is not used

        '<style type="text/css">',
        '.module { position: absolute; }',
        '.title-container { position: absolute; margin-top: 0; margin-bottom: 0;'
                           'display: flex; align-items: center; justify-content: center}',
        '.title-content { margin-top: 0; margin-bottom: 0; }',
        '.element { position: absolute; }',
        'body { margin: 0; }'
        '</style>',

        '</head>',
        ''
    ]
    return "\n".join(header_lines)


def gen_grid_content(module_data):
    body = html_element.gen_images(module_data)
    body += html_element.gen_south_captions(module_data)
    body += html_element.gen_titles(module_data)
    body += html_element.gen_row_titles(module_data)
    body += html_element.gen_column_titles(module_data)
    return body

# def gen_plot_content(module_data, id): # NOTE: currently chartjs is not used
#     body = html_plot.create_canvas(module_data, id)
#     body += html_plot.create_script(module_data, id)
#     return body

def gen_body_content(module_data, offset_top, offset_left, id):
    body = html_element.gen_module_unit_mm(module_data['total_width'], module_data['total_height'], offset_top, offset_left)
    body += gen_grid_content(module_data)
    return body + '\n' + '</div>'

def _export_image(module, figure_idx, module_idx, path, row, col):
    elem = module["elements_content"][row][col]
    width, height = module['element_config']['img_width'], module['element_config']['img_height']

    assert isinstance(elem["image"], ElementData), "Element is of the wrong type."

    prefix = f'img-{row+1}-{col+1}-{figure_idx+1}-{module_idx+1}'
    prefix = os.path.join(path, prefix)

    try:
        elem["image"] = elem["image"].make_html(width, height, prefix)
    except NotImplementedError:
        elem["image"] = elem["image"].make_raster(width, height, prefix)

def export_images(module, figure_idx, module_idx, path):
    threads = []
    for row in range(module["num_rows"]):
        for col in range(module["num_columns"]):
            t = threading.Thread(target=_export_image, args=(module, figure_idx, module_idx, path, row, col))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()

def generate(module_data, figure_idx, module_idx, temp_folder, delete_gen_files=False, tex_packages=[]):
    export_images(module_data, figure_idx, module_idx, path=temp_folder)
    return module_data

def combine(data, filename, temp_folder, delete_gen_files=False):
    html_code = html_header_and_styles()
    html_code += '<body>' + '\n'

    # Create a container div so the result can be embedded
    sum_total_width_mm = 0
    for d in data[0]:
        sum_total_width_mm += d['total_width']
    figure_height = 0.
    for d in data:
        figure_height += d[0]['total_height']
    html_code += f"<div style='position: relative; background-color: white; width: {sum_total_width_mm}mm; height: {figure_height}mm; ' > \n"

    offset_top = 0
    for fig_idx in range(len(data)):
        offset_left = 0
        module_index = 0
        for module in data[fig_idx]:
            html_code += gen_body_content(module, offset_top=offset_top, offset_left=offset_left, id=module_index) + '\n'
            offset_left += module['total_width']
            module_index += 1
        offset_top += data[fig_idx][0]['total_height']

    html_code += '\n' + '</div></body></html>'

    with open(filename, "w") as file:
        file.write(html_code)

    # NOTE: currently chartjs is not used
    # to_path = os.path.dirname(filename)
    # chartjs.emit(to_path)