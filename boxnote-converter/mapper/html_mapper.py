"""
BoxNote to HTML Type Mapper
Author: XZhouQD
Since: Dec 30 2022
"""

from typing import Dict, List
import logging
import pathlib
import requests


logger = logging.getLogger()


base_style = '''<style type="text/css">
table {
    min-width: 500px;
    border: 1px solid #000;
    cellspacing: 0;
    text-align: center;
}
table tr:nth-child(odd) {
    background-color: #ddd;
    border: 1px solid #000;
}
table tr:nth-child(even) {
    background-color: #fff;
    border: 1px solid #000;
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
</style>'''


tag_open_map = {
    'paragraph': '<p style="text-align: {alignment}">',
    #'text': '',
    'strong': '<strong>',
    'em': '<em>',
    'underline': '<u>',
    'strikethrough': '<s>',
    'ordered_list': '<ol>',
    'blockquote': '<blockquote>',
    'bullet_list': '<ul>',
    'list_item': '<li>',
    'check_list': '<ul style="list-style-type:none">',
    'check_list_item': '<li><input type="checkbox" {checked}>[{x}]',
    'horizontal_rule': '<hr/>',
    'table': '<table>',
    'table_row': '<tr>',
    'table_cell': '<td colspan={colspan} rowspan={rowspan} colwidth={colwidth}>',
    'table_header': '<th>',
    'image': '<img src="{src}">',
    'highlight': '<span style="background-color:{color}">',
    'heading': '<h{level}>',
    'font_size': '<span style="font-size:{size}">',
    'font_color': '<span style="color:{color}">',
    'link': '<a href="{href}">',
    'code_block': '<pre><code>',
    'call_out_box': '<span style="background-color:{backgroundColor}">{emoji}'
}

tag_close_map = {
    'paragraph': '</p>',
    #'text': '',
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
    'table': '</table>',
    'table_row': '</tr>',
    'table_cell': '</td>',
    'table_header': '</th>',
    'image': '</img>',
    'highlight': '</span>',
    'heading': '</h{level}>',
    'font_size': '</span>',
    'font_color': '</span>',
    'link': '</a>',
    'horizontal_rule': '',
    'code_block': '</code></pre>',
    'call_out_box': '</span>'
}


def get_tag_open(tag: str, **kwargs) -> str:
    if tag in tag_open_map:
        return tag_open_map[tag].format(**kwargs)
    return None


def get_tag_close(tag: str, **kwargs) -> str:
    if tag in tag_close_map:
        return tag_close_map[tag].format(**kwargs)
    return None


def get_base_style() -> str:
    return base_style


def handle_text_marks(marks: List[Dict], text) -> str:
    tag_starts = [tag_open_map.get(mark['type'], '').format(**mark.get('attrs', {})) for mark in marks]
    tag_ends = [tag_close_map.get(mark['type'], '') for mark in marks[::-1]]
    result = ''.join(tag_starts) + text + ''.join(tag_ends)
    return result


def handle_image(attrs: Dict[str, str], title, workdir, token=None) -> str:
    if token:
        box_file_id = attrs.get('boxFileId')
        box_file_name = attrs.get('fileName')
        logger.info(f'Downloading image {box_file_name}')
        if box_file_id:
            download_image(box_file_id, box_file_name, workdir, token)
            return tag_open_map.get('image').format(src=(workdir / pathlib.Path(f'{box_file_id}_{box_file_name}')).absolute()) \
                   + tag_close_map.get('image')
    file_name = attrs.get('fileName')
    if file_name:
        return tag_open_map.get('image').format(src=(workdir / pathlib.Path(f'Box Notes Images/{title} Images/{file_name}')).absolute()) \
               + tag_close_map.get('image')
    return ''


def download_image(box_file_id: str, file_name: str, workdir, token: str) -> None:
    if not token.startswith("Bearer "):
        token = "Bearer " + token
    headers = {
        'Authorization': token
    }
    url = f'https://api.box.com/2.0/files/{box_file_id}/content'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open((workdir / pathlib.Path(f'{box_file_id}_{file_name}')).absolute(), 'wb') as f:
            f.write(response.content)
    else:
        logger.error(f'Failed to download image {file_name}')
