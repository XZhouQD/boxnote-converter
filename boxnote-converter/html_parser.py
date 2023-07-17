"""
BoxNote to HTML Parser
Author: XZhouQD
Since: Dec 30 2022
"""

import json
from typing import Dict, List, Union
import logging
import mapper.html_mapper as html_mapper
import pathlib


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger()
token = None


def parse(boxnote_content: Union[str, bytes, bytearray], title: str, workdir, access_token=None) -> str:
    """
    Parse BoxNote to HTML
    """
    global token
    token = access_token if access_token else token
    try:
        boxnote = json.loads(boxnote_content)
    except json.JSONDecodeError as e:
        logger.error('Invalid BoxNote content: JSON parse failed')
        raise e
    
    if 'doc' not in boxnote:
        logger.error('Invalid BoxNote content: no doc field')
        raise ValueError('Invalid BoxNote content: no doc field')

    if 'content' not in boxnote.get('doc', {}):
        logger.error('Invalid BoxNote content: no content field')
        raise ValueError('Invalid BoxNote content: no content field')

    contents = ['<!DOCTYPE html>', '<html>', f'{html_mapper.get_base_style()}', '<head>', '<meta charset="UTF-8">', f'<title>{title}</title>', '</head>', '<body>']

    parse_content(boxnote.get('doc', {}).get('content', {}), contents, title, workdir)

    contents = list(filter(lambda x: x is not None, contents))
    result = '\n'.join(contents)
    result = str.replace(result, '<p style="text-align: left">\n</p>', '')
    return result


def parse_content(content: Union[Dict, List], contents: List[str], title, workdir, ignore_paragraph=False) -> None:
    """
    Parse BoxNote content
    """
    if not content:
        return

    if isinstance(content, list):
        for item in content:
            parse_content(item, contents, title, workdir, ignore_paragraph)
        return

    if not isinstance(content, dict):
        return

    if 'type' not in content:
        logger.error('Invalid BoxNote content: no type field')
        raise ValueError('Invalid BoxNote content: no type field')
    
    type_tag = content.get('type', '')
    if type_tag == 'paragraph':
        if not ignore_paragraph:
            alignment = 'left'
            marks = content.get('marks', [])
            for mark in marks:
                if mark.get('type', '') == 'alignment':
                    alignment = mark.get('attrs', {}).get('alignment', '')
            contents.append(html_mapper.get_tag_open('paragraph', alignment=alignment))
            parse_content(content.get('content', []), contents, title, workdir)
            contents.append(html_mapper.get_tag_close('paragraph'))
        else:
            parse_content(content.get('content', []), contents, title, workdir)
    elif type_tag == 'text':
        contents.append(html_mapper.get_tag_open('text'))
        contents.append(html_mapper.handle_text_marks(content.get('marks', []), content.get('text', '')))
        contents.append(html_mapper.get_tag_close('text'))
    elif type_tag == 'check_list_item':
        args = {'checked': 'checked' if content['attrs']['checked'] else '', 'x': 'X' if content['attrs']['checked'] else '  '}
        contents.append(html_mapper.get_tag_open('check_list_item', **args))
        parse_content(content.get('content', []), contents, title, workdir, ignore_paragraph=True)
        contents.append(html_mapper.get_tag_close('check_list_item'))
    elif type_tag in ['list_item', 'table_cell', 'call_out_box']:
        contents.append(html_mapper.get_tag_open(type_tag, **content.get('attrs', {})))
        parse_content(content.get('content', []), contents, title, workdir, ignore_paragraph=True)
        contents.append(html_mapper.get_tag_close(type_tag, **content.get('attrs', {})))
    elif type_tag == 'image':
        contents.append(html_mapper.handle_image(content.get('attrs', {}), title, workdir, token))
    elif type_tag in ['strong', 'em', 'underline', 'strikethrough', 'ordered_list', 'bullet_list', 'blockquote', 'code_block', 
                      'check_list', 'table', 'table_row', 'heading', 'link', 'font_size', 'font_color', 'horizontal_rule']:
        contents.append(html_mapper.get_tag_open(type_tag, **content.get('attrs', {})))
        parse_content(content.get('content', []), contents, title, workdir)
        contents.append(html_mapper.get_tag_close(type_tag, **content.get('attrs', {})))
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('-d', '--dir', help='Work directory')
    parser.add_argument('-t', '--token', nargs='?', help='Box access token', )
    args = parser.parse_args()
    workdir = pathlib.Path(args.dir) if args.dir else pathlib.Path.cwd()
    input_file = workdir / pathlib.Path(args.input)
    with open(input_file, 'r') as f:
        content = f.read()
    title = input_file.stem
    output_file = workdir / pathlib.Path(f'{title}.html')
    with open(output_file, 'w') as f:
        f.write(parse(content, title, workdir, args.token if args.token else None))
