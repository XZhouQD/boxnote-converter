"""
BoxNote to HTML Type Mapper
Author: XZhouQD
Since: Dec 30 2022
"""

from typing import Dict, List
import logging


logger = logging.getLogger()


base_style = '''<style type="text/css">
table {
    min-width: 500px;
    border: 1px solid #ccc;
    cellspacing: 0;
    text-align: center;
}
table tr:nth-child(odd) {
    background-color: #ddd;
}
table tr:nth-child(even) {
    background-color: #fff;
}
table tr :hover {
    background-color: #66ccff;
}
blockquote {
    display: block;
    border-left: 6px solid #d3d3d3;
    padding-left: 16px;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 40px;
    margin-inline-end: 40px;
}
</style>
'''


tag_open_map = {
    'paragraph': '<p>',
    'text': '<span>',
    'strong': '<strong>',
    'em': '<em>',
    'underline': '<u>',
    'strikethrough': '<s>',
    'ordered_list': '<ol>',
    'blockquote': '<blockquote>',
    'bullet_list': '<ul>',
    'list_item': '<li>',
    'check_list': '<ul style="list-style-type:none">',
    'check_list_item': '<li><input type="checkbox">',
    'check_list_item_checked': '<li><input type="checkbox" checked>',
    'table': '<table>',
    'table_row': '<tr>',
    'table_cell': '<td colspan={colspan} rowspan={rowspan} colwidth={colwidth}>',
    'table_header': '<th>',
    'image': '<img src="{src}">',
    'highlight': '<mark style="background-color:{color}">',
    'heading': '<h{level}>',
    'font_size': '<span style="font-size:{size}">',
    'font_color': '<span style="color:{color}">',
    'link': '<a href="{href}">'
}

tag_close_map = {
    'paragraph': '</p>',
    'text': '</span>',
    'strong': '</strong>',
    'em': '</em>',
    'underline': '</u>',
    'strikethrough': '</s>',
    'ordered_list': '</ol>',
    'blockquote': '</blockquote>',
    'bullet_list': '</ul>',
    'list_item': '</li>',
    'check_list': '</ul>',
    'check_list_item': '</li>',
    'check_list_item_checked': '</li>',
    'table': '</table>',
    'table_row': '</tr>',
    'table_cell': '</td>',
    'table_header': '</th>',
    'image': '</img>',
    'highlight': '</mark>',
    'heading': '</h{level}>',
    'font_size': '</span>',
    'font_color': '</span>',
    'link': '</a>'
}


def get_tag_open(tag: str, **kwargs) -> str:
    if tag in tag_open_map:
        return tag_open_map[tag].format(**kwargs)
    return ''


def get_tag_close(tag: str, **kwargs) -> str:
    if tag in tag_close_map:
        return tag_close_map[tag].format(**kwargs)
    return ''


def get_base_style() -> str:
    return base_style


def handle_text_marks(marks: List[Dict], text) -> str:
    tag_starts = [tag_open_map.get(mark['type'], '').format(**mark.get('attrs', {})) for mark in marks]
    tag_ends = [tag_close_map.get(mark['type'], '') for mark in marks[::-1]]
    result = ''.join(tag_starts) + text + ''.join(tag_ends)
    logger.info(result)
    return result


def handle_image(attrs: Dict[str, str], title) -> str:
    file_name = attrs.get('fileName')
    if file_name:
        return tag_open_map.get('image').format(src=f'Box Notes Images/{title} Images/{file_name}') \
               + tag_close_map.get('image')
    # box_shared_link = attrs.get('boxSharedLink')
    # if box_shared_link:
    #     return tag_open_map.get('image').format(src=box_shared_link) + tag_close_map.get('image')
    return ''

