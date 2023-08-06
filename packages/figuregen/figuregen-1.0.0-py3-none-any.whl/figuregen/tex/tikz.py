from . import calculate
import numpy as np

# BEGIN minor utitities for TIKZ generation
def text_umlaut_replacement():
    return {
        "ü": '\\\"u',
        "ö": '\\\"o',
        "ä": '\\\"a',
        "Ü": '\\\"U',
        "Ö": '\\\"O',
        "Ä": '\\\"A',
    }

def replace_all_umlaute(text):
    table = text_umlaut_replacement()

    result = text
    for (placeholder, value) in table.items():
        result = result.replace(placeholder, value)

    return result

def read_optional(data, key, default=None):
    try:
        return data[key]
    except KeyError:
        return default

def is_horizontal(position):
    position0 = position.split(' ')[0]
    if position0=='south' or position0=='north':
        return True
    return False

def is_vertical(position):
    return not is_horizontal(position)

_opposite_map = {
    'west': 'east',
    'east': 'west',
    'north': 'south',
    'south': 'north',
    'north east': 'south west',
    'south west': 'north east',
    'south east': 'north west',
    'north west': 'south east'
}

def opposite(position):
    return _opposite_map[position]

def load_nth_color(color_list, num, idx):
    import numpy as np

    # convert to numpy array to determine shape and force proper data type
    color_array = np.array(color_list, dtype=int)

    if np.any(color_array > 255) or np.any(color_array < 0):
        raise 'Invalid color values'

    if color_array.shape == (3,):
        return color_list # single color
    elif color_array.shape[1] == 3 and color_array.shape[0] >= num:
        return color_list[idx] # ith color of list
    else:
        raise 'Number of colors does not match the number of rows / columns'

def gen_tikZ_frame(rgb_list, line_width):
    color = gen_tikZ_rgb255(rgb_list)
    return 'draw='+color+', line width='+str(line_width)+', '

def gen_tikZ_rgb255(rgb_list):
    return '{rgb,255:red,'+str(rgb_list[0])+';green,'+str(rgb_list[1])+';blue,'+str(rgb_list[2])+'}'

def gen_LaTeX_fontsize(fontsize, line_space):
    line_space = float(fontsize) * line_space
    return '\\fontsize{'+str(fontsize)+'pt}{'+str(fontsize)+'pt}'
# END minor utitities for TIKZ generation


# GENERATING TIKZ NODES
### BEGIN generating basic nodes ###
def gen_plain_node(width, height, name, parent_name = None, position = None, anchor='center', additional_params=''):
    '''
    Creates code for a TikZ node. A 'plain' node is a node that does not hold any information 
    (no text, no img), so its mostly used to generate offsets.
    additional params: e.g. 'fill=blue, ' or 'draw, '. You can also combine them like 'fill=blue, draw, '. 
            Important is, that you do not forget the comma at the end.
    '''
    pos = '(0,0)'
    if parent_name and position:
        pos = '('+ parent_name + '.' + position +')'

    return '\\node[anchor='+ anchor +', minimum width='+ str(width) +'mm, minimum height='+ str(height) +'mm, ' \
        + additional_params+' inner sep=0, outer sep=0] ('+ name +') at ' + pos + ' {}; \n'

def gen_text_node(width, height, text, parent_name, fontsize, position='center', anchor='center', 
                alignment='centering', rotation=0, text_color=None, vert_algin='c'):
    '''
    Creates a node that contains text-based content. In case, the text does not fit in a box of given 
    width and height, the text is 'clipped off'. This makes sure that the text-field has the correct 
    size.
    '''
    comment = '% Begin text node: we clip the text, so that it will not overlap with other content.\n'
    begin_clipping = '\\begin{scope}\n\\clip ('+parent_name+'.south west) rectangle ('+\
                        parent_name+'.north east);\n'
    type_field = parent_name.split('-')[0]

    if rotation != 0:
        if type_field=='east' or type_field=='west':
            width, height = height, width

    txt_color=''
    if text_color is not None and text_color!=[0,0,0]:
        txt_color='text='+gen_tikZ_rgb255(text_color)+', '

    paddedtext = replace_all_umlaute(text)
    # ensure that all lines are of equal height
    paddedtext = paddedtext.replace("\n", "\\strut\\\\")
    paddedtext += "\\strut"

    if alignment == "left":
        alignment = "raggedright"
    elif alignment == "right":
        alignment = "raggedleft"
    elif alignment != "centering":
        raise ValueError("alignment")

    node = f'\\node[anchor={anchor}, minimum width={width}mm, minimum height={height}mm, '\
        f'rotate={rotation}, {txt_color}inner sep=0, outer sep=0] at ({parent_name}.{position}) \n'
    node_content = '{\\begin{minipage}['+vert_algin+']['+str(height)+'mm]{'+str(width)+'mm} '+\
                    fontsize + ' \\selectfont \\'+alignment+' \n'+paddedtext+'\n\\end{minipage}};\n'
    end_clipping = '\\end{scope}\n'
    comment_2 = '% End text node\n'

    return comment + begin_clipping + node + node_content + end_clipping + comment_2 +'\n'

def gen_line_node(parent_name, lines, rel_p_factor):
    '''
        We need to create a node to clip the drawn line within a node.
        For exmaple, if we want to draw on top of an image, we clip the drawing.
    '''
    comment = '% Begin clipped line: draw a line on top of an image.\n'
    begin_clipping = '\\begin{scope}\n\\clip ('+parent_name+'.south west) rectangle ('+parent_name+\
                    '.north east);\n'

    drawn_lines = ''
    for line in lines:
        start = np.array(line['from']) * rel_p_factor
        end = np.array(line['to']) * rel_p_factor
        color = line['color']
        if color is None or color == [0,0,0]:
            tmp_color = ''
        else:
            tmp_color = r'\definecolor{tempcolor}{RGB}{'+ f'{color[0]}, {color[1]}, {color[2]}' +'}\n'

        draw_color = 'tempcolor, ' if tmp_color != '' else ''
        drawn_lines += tmp_color + f"\\draw[{draw_color}line width={line['lw']}] ([xshift={start[1]}mm, "\
                    f"yshift=-{start[0]}mm]{parent_name}.north west) -- ([xshift={end[1]}mm, "\
                    f"yshift=-{end[0]}mm]{parent_name}.north west);\n"
    
    end_clipping = '\\end{scope}\n'
    comment_2 = '% End clipped line\n'
    return comment + begin_clipping + drawn_lines + end_clipping + comment_2 + '\n'

def gen_clipped_img_node(width, height, img_path, name, frame_width_pt, parent_name=None, position=None, anchor='center'):
    '''
    This function will be used, if the image has a frame. We clip the image.
    '''
    comment = '% Begin clipped image: Because of round-off errors, frames would sometimes not cover the borders of the image. Therefore, we clip the image slightly.\n'
    img_body = gen_plain_node(width, height, name, parent_name, position, anchor)
    fwpt = str(frame_width_pt * 0.5)
    begin_clipping = '\\begin{scope}\n\\clip ([xshift = '+fwpt+'pt, yshift = '+fwpt+'pt]'+name+'.south west) rectangle '\
                        '([xshift = -'+fwpt+'pt, yshift = -'+fwpt+'pt]'+name+'.north east);\n'
    img_content = gen_img_node(width, height, img_path, name+'-content', parent_name, position, anchor)
    end_clipping = '\\end{scope}\n'
    comment_2 = '% End clipped image\n'
    return comment + img_body + begin_clipping + img_content + end_clipping + comment_2 + '\n'

def gen_img_node(width, height, img_path, name, parent_name=None, position=None, anchor='center'):
    '''
    Creates a node that contains an image. No cropping will be done to the image: The image can 
    be distorted, if the width/height ratio is not fitted proberly.

    addtional params: e.g. 'draw=blue, line width=0.3mm, ' If you want an RGB color, there are 
                    functions provided that generates Tikz-friendly 'code'.
    '''
    pos = '(0,0)'
    if parent_name and position:
        pos = '('+ parent_name + '.' + position +')'

    # make sure the path is LaTeX compatible
    img_path = img_path.replace('\\', '/')

    return '\\node[anchor='+ anchor +', minimum width='+ str(width) +'mm, '\
            'minimum height='+ str(height) +'mm, inner sep = 0, outer sep = 0] ('+ name +') at '+ pos +\
            ' {\\includegraphics[width='+str(width)+'mm, height='+str(height)+'mm]{\\detokenize{'+ img_path +'}}}; \n'

def gen_img_helper(elem, img_width, img_height, append, parent_name, position, anchor):
    '''
    If the image has a frame: 
        Because of round-off errors, frames would sometimes not cover the borders of the image. 
        Therefore, we clip the image slightly.
    else:
        simple image node

    This does not contain the frame node.
    '''
    frame_specs = read_optional(elem, 'frame', default='')
    if frame_specs != '':
        return gen_clipped_img_node(img_width, img_height, name='img-'+append, 
                                frame_width_pt=frame_specs['line_width'], parent_name=parent_name, 
                                position=position, anchor=anchor, img_path=elem['image'])
    return gen_img_node(img_width, img_height, name='img-'+append, parent_name=parent_name, 
                                position=position, anchor=anchor, img_path=elem['image'])

def gen_frame_node(parent_width, parent_height, parent_name, color, linewidth):
    '''
    Because frames in tikz ignore borders per default, we sometimes have incorrect 'total_width' and 
    'total_height'. To prevent that, we draw frames on top of an existing node and take the linewidth
    into account, so that frames do not overlap with other elements or even worse, goes 'beyond the 
    total width and height' of the figure.
    '''
    if color == None or linewidth == 0:
        return ''
    frame_prop = gen_tikZ_frame(color, linewidth)
    linewidth_mm = calculate.pt_to_mm(linewidth)
    width = parent_width - linewidth_mm
    height = parent_height - linewidth_mm
    name = parent_name.replace('img', 'frame')
    return gen_plain_node(width, height, name, parent_name, position='center', anchor='center', 
                        additional_params=frame_prop)
### END generating basic nodes ###


### BEGIN helper node functions ###
def gen_node_north(width, height, name, parent_name, offset, offset_name, content='', fontsize=8, 
                    alignment='centering', rotate_text=0, background_color=None, text_color=None):
    return gen_node_helper('north', 'south', **locals())

def gen_node_south(width, height, name, parent_name, offset, offset_name, content='', fontsize=8, 
                    alignment='centering', rotate_text=0, background_color=None, text_color=None):
    return gen_node_helper('south', 'north', **locals())

def gen_node_west(width, height, name, parent_name, offset, offset_name, content='', fontsize=8, 
                    alignment='centering', rotate_text=90, background_color=None, text_color=None):
    return gen_node_helper('west', 'east', **locals())

def gen_node_east(width, height, name, parent_name, offset, offset_name, content='', fontsize=8, 
                    alignment='centering', rotate_text=90, background_color=None, text_color=None):
    return gen_node_helper('east', 'west', **locals())

def gen_node_helper(position, anchor, width, height, name, parent_name, offset, offset_name, content,
                    fontsize, alignment='centering', rotate_text=0, background_color=None, text_color=None):
    space_node = ''
    if offset > 0.0: # offset node
        if offset_name is None:
            offset_name = name+'-space'

        space_node = gen_plain_node(width=0.0, height=offset, name=offset_name, parent_name=parent_name, 
                                    position=position, anchor=anchor)
        if is_vertical(position) or 'west-group-field' in name or 'east-group-field' in name:
            space_node = gen_plain_node(width=offset, height=0.0, name=offset_name, 
                                        parent_name=parent_name, position=position, anchor=anchor)

        parent_name = offset_name

    # container node
    bg_color=''
    if background_color is not None:
        bg_color='fill='+gen_tikZ_rgb255(background_color)+', '
    container_node = gen_plain_node(width, height, name=name, parent_name=parent_name, position=position,
                                     anchor=anchor, additional_params=bg_color)

    # text/content node
    content_node = ''
    if content != '':
        content_node = gen_text_node(width, height, content, parent_name=name, position='center', 
                                    anchor='center', fontsize=fontsize, alignment=alignment,
                                    rotation=rotate_text, text_color=text_color)

    return space_node + container_node + content_node

def get_box_anchor_and_position(alignment):
    if alignment == 'left':
        txt_box_pos = 'east'
        txt_box_anchor = 'east'
    elif alignment == 'right':
        txt_box_pos = 'west'
        txt_box_anchor = 'west'
    else:
        txt_box_pos = 'center'
        txt_box_anchor = 'center'
    return txt_box_pos, txt_box_anchor

def gen_label_helper(position, width, height, name, parent_name, text_offset, content, fontsize, 
                    alignment='centering', background_color=None, text_color=None, vert_align='c'):
    anchor = position
    position = opposite(position)

    # container node
    bg_color=''
    if background_color is not None:
        bg_color='fill='+gen_tikZ_rgb255(background_color)+', '
    container_node = gen_plain_node(width, height, name=name, parent_name=parent_name, position=position,
                                     anchor=anchor, additional_params=bg_color)

    # text/content node
    content_node = ''
    if content != '':
        #pos1, anch1 = get_box_anchor_and_position(alignment)
        pos1, anch1 = 'center', 'center' # works better
        content_node = gen_text_node(width-text_offset, height-text_offset, content, parent_name=name, 
                                    position=pos1, anchor=anch1, fontsize=fontsize, alignment=alignment,
                                    rotation=0, text_color=text_color, vert_algin=vert_align)

    return container_node + content_node + '\n'
### END helper node functions ###


### BEGIN space/padding nodes ###
def add_outer_horizontal_padding(margin, num_columns, position, has_title, has_row_field):
    '''
    Adds a padding between title (or other outer content) and the edge of the figure if so desired.
    '''
    if position=='east':
        parent_name = position+'-field-1-'+str(num_columns)
    else: # west
        parent_name = position+'-field-1-1'

    if has_title:
        parent_name = position+'-group-field'
    elif has_row_field:
        parent_name = position+'-row-field-1'

    return gen_space_helper(margin, parent_name, position)

def add_outer_vertical_padding(margin, position, num_rows, has_title, has_column_field):
    '''
    Adds a padding between title (or other outer content) and the edge of the figure if so desired.
    '''
    if position=='south':
        parent_name = position+'-field-'+str(num_rows)+'-1'
    else: # north
        parent_name = position+'-field-1-1'

    if has_title:
        parent_name = position+'-group-field'
    elif has_column_field:
        parent_name = position+'-column-field-1'

    return gen_space_helper(margin, parent_name, position)

def gen_space_helper(margin, parent_name, position):
    '''
    Only manages the outer padding ('top', 'bottom', 'left', 'right')
    '''
    if margin==0.0:
        return ''
    name = position+'-space'

    if is_vertical(position):
        width, height = margin, 0.0
    else:
        width, height = 0.0, margin

    return gen_node_helper(position, opposite(position), width, height, name, parent_name, 
                            offset=0.0, offset_name=None, content='', fontsize='')

def add_all_outer_paddings(data):
    padding_nodes = add_outer_horizontal_padding(margin=data['padding']['west'], position='west', 
                            num_columns=data['num_columns'], has_title=(data['titles']['west']['width']!=0.0),
                            has_row_field=(data['row_titles']['west']['width']!=0.0))
    padding_nodes += add_outer_horizontal_padding(margin=data['padding']['east'], position='east', 
                            num_columns=data['num_columns'], has_title=(data['titles']['east']['width']!=0.0), 
                            has_row_field=(data['row_titles']['east']['width']!=0.0))
    padding_nodes += add_outer_vertical_padding(margin=data['padding']['north'], position='north', 
                            num_rows=data['num_rows'], has_title=(data['titles']['north']['height']!=0.0), 
                            has_column_field=(data['column_titles']['north']['height']!=0.0))
    padding_nodes += add_outer_vertical_padding(margin=data['padding']['south'], position='south', 
                            num_rows=data['num_rows'], has_title=(data['titles']['south']['height']!=0.0), 
                            has_column_field=(data['column_titles']['south']['height']!=0.0))
    return padding_nodes
### END space/padding nodes ###


### BEGIN generating titles (figure title + row/column titles) ###
def gen_horizontal_figure_title(position, num_rows, width, title_config, column_config, 
                                txt_alignment='centering'):
    if title_config['height']==0.0:
        return ''

    if position=='south':
        parent_name = position+'-field-'+str(num_rows)+'-1'
        name='south-group-field'
    else: #north
        parent_name = position+'-field-1-1'
        name='north-group-field'

    if column_config['height']!=0.0:
        parent_name = position+'-column-field-1'

    anchor = opposite(position)+' west'
    position = position+' west'

    fontsize = gen_LaTeX_fontsize(title_config['fontsize'],title_config['line_space'])

    return gen_node_helper(position, anchor, width, title_config['height'], name=name, 
                        parent_name=parent_name, offset=title_config['offset'], offset_name=None,
                        content=title_config['content'], fontsize=fontsize, alignment=txt_alignment,
                        rotate_text=title_config['rotation'], background_color=title_config['background_color'], 
                        text_color=title_config['text_color'])

def gen_vertical_figure_title(position, num_columns, height, title_config, title_offset, column_north_config, txt_alignment='centering'):
    '''
    Update: east/west titles start and end with the first and last image. The last 'south' captions, 
    as well as column titles are not anymore included!
    We still create north-field as a parent, because this field does not do anything (not further supported).

    Note: provided offset is already the calculated offset from the image (+ row titles) up to it's own offset
    '''
    if title_config['width']==0.0:
        return ''

    if position=='east':
        supplement = str(num_columns)
        name='east-group-field'
    else: #west
        supplement = '1'
        name='west-group-field'
    parent_name = 'north-field-1-' + supplement

    anchor = 'north '+opposite(position)
    position = 'north '+position
    fontsize = gen_LaTeX_fontsize(title_config['fontsize'],title_config['line_space'])

    return gen_node_helper(position, anchor, title_config['width'], height, name=name, 
                        parent_name=parent_name, offset=title_offset, offset_name=None,
                        content=title_config['content'], fontsize=fontsize, alignment=txt_alignment,
                        rotate_text=title_config['rotation'], background_color=title_config['background_color'],
                        text_color=title_config['text_color'])

def gen_outer_row(position, row, data):
    '''
    Generates titles for each row: can be placed on the left and/or right side of the image blocks
    '''
    row_title = data['row_titles'][position]
    if row_title['width']==0.0:
        return ''

    name=position+'-row-field-'+str(row)
    parent_name='west-field-'+str(row)+'-1'
    if position=='east':
        parent_name='east-field-'+str(row)+'-'+str(data['num_columns'])

    bg_color_list = read_optional(row_title, 'background_colors', default=None)
    if bg_color_list is not None:
        bg_color = load_nth_color(bg_color_list, data['num_rows'], row-1)
    else:
        bg_color = None

    return gen_node_helper(position, opposite(position), row_title['width'], 
                        data['element_config']['img_height'], name=name, parent_name=parent_name, 
                        offset=row_title['offset'], offset_name=None, content=row_title['content'][row-1], 
                        fontsize=gen_LaTeX_fontsize(row_title['fontsize'],row_title['line_space']), 
                        alignment='centering', rotate_text=row_title['rotation'], 
                        background_color=bg_color, text_color=row_title['text_color'])

def gen_outer_col(position, column, data):
    '''
    Generates titles for each column: can be placed on top and/or at the bottom of the image blocks
    '''
    col_title = data['column_titles'][position]

    if col_title['height']==0.0:
        return ''

    name=position+'-column-field-'+str(column)
    parent_name='north-field-1-'+str(column)
    if position=='south':
        parent_name='south-field-'+str(data['num_rows'])+'-'+str(column)

    bg_color_list = read_optional(col_title, 'background_colors', default=None)
    if bg_color_list is not None:
        bg_color = load_nth_color(bg_color_list, data['num_columns'], column-1)
    else:
        bg_color = None

    fontsize = gen_LaTeX_fontsize(col_title['fontsize'],col_title['line_space'])

    return gen_node_helper(position, opposite(position), data['element_config']['img_width'], 
                    col_title['height'], name=name, parent_name=parent_name, offset=col_title['offset'], 
                    offset_name=None, content=col_title['content'][column-1], fontsize=fontsize, 
                    alignment='centering', rotate_text=col_title['rotation'], background_color=bg_color, 
                    text_color=col_title['text_color'])

def add_col_and_row_titles(data):
    c_r_title_nodes = ''

    for column in range(data['num_columns']):
        c_r_title_nodes += gen_outer_col('south', column+1, data)
        c_r_title_nodes += gen_outer_col('north', column+1, data)

    for row in range(data['num_rows']):
        c_r_title_nodes += gen_outer_row('west', row+1, data)
        c_r_title_nodes += gen_outer_row('east', row+1, data)

    return c_r_title_nodes

def add_big_titles(data):
    body_width = calculate.get_body_width(data)
    body_height = calculate.get_body_height(data)

    # horizontal
    title_nodes = gen_horizontal_figure_title('north', num_rows=data['num_rows'], width=body_width, 
                                title_config=data['titles']['north'], 
                                column_config=data['column_titles']['north'])
    title_nodes += gen_horizontal_figure_title('south', num_rows=data['num_rows'], width=body_width, 
                                title_config=data['titles']['south'],
                                column_config=data['column_titles']['south'])

    # vertical
    offset_west_title = calculate.get_h_offset_for_title(title_offset=data['titles']['west']['offset'], 
                                        caption_config=data['element_config']['captions']['west'],
                                        row_config=data['row_titles']['west'])
    title_nodes += gen_vertical_figure_title('west', num_columns=data['num_columns'], height=body_height, 
                                        title_config=data['titles']['west'], 
                                        title_offset=offset_west_title, 
                                        column_north_config=data['column_titles']['north'])
    offset_east_title = calculate.get_h_offset_for_title(title_offset=data['titles']['east']['offset'], 
                                        caption_config=data['element_config']['captions']['east'],
                                        row_config=data['row_titles']['east'])
    title_nodes += gen_vertical_figure_title('east', num_columns=data['num_columns'], height=body_height, 
                                        title_config=data['titles']['east'],
                                        title_offset=offset_east_title, 
                                        column_north_config=data['column_titles']['north'])
    return title_nodes
### END generating titles (figure title + row/column titles) ###


### BEGIN generating img/element blocks ###
def gen_all_image_blocks(data):
    '''
    Generates tikz nodes for each element/image based on the number of columns and rows
    '''
    content = ''
    rowIndex = 1
    for row in data['elements_content']:
        colIndex = 1
        for elem in row:
            if colIndex<=data['num_columns']:
                content += gen_one_img_block(data, rowIndex, colIndex)
                colIndex += 1
        rowIndex += 1
    return content

def draw_rectangle_on_img(parent_name, crop_num, rel_width, rel_height, pos_x1, pos_y1, xoffset, 
                            yoffset, line_width, color=[255,255,255], dashed=False):

    offset_node = gen_plain_node(width=rel_width * pos_x1,height=rel_height * pos_y1,
                                name='inset'+str(crop_num)+'-offset-'+parent_name, parent_name=parent_name,
                                position= "north west", anchor="north west", additional_params='')

    draw_params = 'draw='+str(gen_tikZ_rgb255(color))+', line width='+str(line_width)+'pt, '
    if dashed:
        draw_params = draw_params + 'dashed, '

    inset_node = gen_plain_node(width=rel_width * (xoffset),height=rel_height *(yoffset),
                            name='inset'+str(crop_num)+'-'+parent_name,
                            parent_name='inset'+str(crop_num)+'-offset-'+parent_name, 
                            position= "south east", anchor="north west",
                            additional_params=draw_params)
    return offset_node + inset_node

def gen_marker_nodes(markers, parent_name, rel_width, rel_height):
    marker_nodes = ''
    crop_num = 0
    for m in markers:
        crop_num += 1
        pos_x1, pos_y1 = m['pos'][0], m['pos'][1]
        xoffset, yoffset = m['size'][0], m['size'][1]  
        marker_nodes += draw_rectangle_on_img(parent_name, crop_num, rel_width, rel_height,
                                            pos_x1, pos_y1,xoffset, yoffset, line_width=m['lw'], 
                                            color=m['color'], dashed=m['dashed'])
    return marker_nodes

def make_label(dir, cfg, name, parent_name):
    try:
        cfg = cfg[name]
    except KeyError:
        return ''

    # set the text alignment
    alignment_lookup = {
        'south': 'centering',
        'north': 'centering',
        'east': 'right',
        'west': 'left'
    }
    alignment = alignment_lookup[dir.split(' ')[-1]]

    # generate unique identifier based on row and column index
    p_name_split = parent_name.split('-')
    unique_id = p_name_split[-2] + '-' + p_name_split[-1]
    node_name = f'label-{dir}-' + unique_id
    offset_name = node_name +'-space'

    # determine the correct offsets depending on wether it is in the corner or center
    if 'east' in dir or 'west' in dir:
        offset_w, offset_h = cfg['offset_mm'][0], cfg['offset_mm'][1]
    else:
        offset_w, offset_h = 0, cfg['offset_mm']

    # determine vertical alignment based on label position (top vs bottom)
    vert_pos = name.split('_')[0]
    if vert_pos == 'top' or vert_pos == 'bottom':
        vert_align = vert_pos[0]
    else:
        vert_align = 'c' #should never be the case, however this value is still valid

    result = ""
    result += gen_plain_node(offset_w, offset_h, offset_name, parent_name, dir, dir)
    result += gen_label_helper(dir, cfg['width_mm'], cfg['height_mm'], node_name, offset_name, 
                        cfg['padding_mm'], cfg['text'], gen_LaTeX_fontsize(cfg['fontsize'], 
                        cfg['line_space']), alignment, cfg['background_color'], cfg['text_color'], 
                        vert_align=vert_align)
    return result

def gen_label(label_config, parent_name):
    l_content = ''
    l_content += make_label('north', label_config, 'top_center', parent_name)
    l_content += make_label('south', label_config, 'bottom_center', parent_name)
    l_content += make_label('north east', label_config, 'top_right', parent_name)
    l_content += make_label('south east', label_config, 'bottom_right', parent_name)
    l_content += make_label('north west', label_config, 'top_left', parent_name)
    l_content += make_label('south west', label_config, 'bottom_left', parent_name)

    return l_content + '\n'

def gen_one_img_block(data, row, col):
    '''
    An image block contains a node for the image.
    Optional: An image block can additionally contain a south caption, frames, markers (rectangle) 
    and lines.
    
    Note: We still create north/east/west nodes (empty!) on each side of the image, because we append 
        other nodes on them. This also allows - if so desired - to extend the image block, such 
        that an image can have captions at north/west/east side.
    '''
    img_width = data['element_config']['img_width']
    img_height = data['element_config']['img_height']
    capt_config = data['element_config']['captions']['south']
    elem = data['elements_content'][row-1][col-1]
    south_caption = elem['captions']['south']

    append = str(row)+'-'+str(col)

    # create image block
    tikz_content = ''

    if col == 1: # create img block from top

        if row == 1: # create the very first node
            tikz_content += gen_plain_node(img_width, height=0.0, name='north-field-'+append)
        else: #coming from top, meaning, we create a new row with corresponding row spacing
            tikz_content += gen_node_south(img_width, height=0.0, name='north-field-'+append, 
                                        parent_name='south-field-'+str(row-1)+'-'+str(col),
                                        offset=data['row_space'],
                                        offset_name='row-space-'+str(row-1)+'-'+str(row))
        parent_name='north-field-'+append

        tikz_content += gen_img_helper(elem, img_width, img_height, append, parent_name, position='south', anchor='north')
        tikz_content += gen_node_west(width=0.0, height=img_height, name='west-field-'+append, 
                                    parent_name='img-'+append, offset=0.0, offset_name=None)

    else: # creating img block from left, add corresponding column spacing
        tikz_content += gen_node_east(width=0.0, height=img_height, name='west-field-'+append, 
                                    parent_name='east-field-'+str(row)+'-'+str(col-1),
                                    offset=data['column_space'], 
                                    offset_name='column-space-'+str(row)+'-'+str(col-1)+'-'+str(col))

        parent_name='west-field-'+append
        tikz_content += gen_img_helper(elem, img_width, img_height, append, parent_name, position='east', anchor='west')
        tikz_content += gen_node_north(img_width, height=0.0, name='north-field-'+append, 
                                    parent_name='img-'+append, offset=0.0, offset_name=None)

    # creating east and south nodes are independent of where the parent node was appended
    tikz_content += gen_node_east(width=0.0, height=img_height, name='east-field-'+append, 
                                    parent_name='img-'+append, offset=0.0, offset_name=None)

    #south caption
    tikz_content += gen_node_south(img_width, height=capt_config['height'], name='south-field-'+append, 
                                parent_name='img-'+append, offset=capt_config['offset'], offset_name=None, 
                                content=south_caption, 
                                fontsize=gen_LaTeX_fontsize(capt_config['fontsize'],capt_config['line_space']),
                                alignment='centering', rotate_text=capt_config['rotation'], 
                                background_color=None, text_color=capt_config['text_color'])

    # optional: add markers, labels, frames, or lines
    marker_specs = read_optional(elem, 'marker', default='')
    if marker_specs != '':
        rel_w, rel_h = calculate.relative_position(data['img_width_px'], data['img_height_px'], 
                                                    img_width, img_height)
        tikz_content += gen_marker_nodes(marker_specs, parent_name='img-'+append, rel_width=rel_w, 
                                        rel_height=rel_h)

    label_specs = read_optional(elem, 'label', default='')
    if label_specs != '':
        tikz_content += gen_label(label_specs, parent_name='img-'+append)

    frame_specs = read_optional(elem, 'frame', default='')
    if frame_specs != '':
        tikz_content += gen_frame_node(img_width, img_height, parent_name='img-'+append, 
                                    color=frame_specs['color'], linewidth=frame_specs['line_width'])

    line_specs = read_optional(elem, 'lines', default='')
    if line_specs != '':
        rel_w, rel_h = calculate.relative_position(data['img_width_px'], data['img_height_px'], 
                                                    img_width, img_height)
        tikz_content += gen_line_node('img-'+append, line_specs, rel_w)

    return tikz_content + '\n'

### END generating img/element blocks ###
# END TIKZ GEN