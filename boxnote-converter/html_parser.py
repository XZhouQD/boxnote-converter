"""
BoxNote to HTML Parser
Author: XZhouQD
Since: Dec 30 2022
"""

import json
from typing import Dict, List, Union
import logging
import mapper.html_mapper as html_mapper
from pathlib import Path


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger()
token = None
user = None


def parse(
        boxnote_content: Union[str, bytes, bytearray],
        title: str,
        workdir: Path,
        access_token: str = None,
        user_id: str = None) -> str:
    """
    Parse BoxNote to HTML
    """
    global token
    token = access_token if access_token else token
    global user
    user = user_id if user_id else user
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
    contents.extend(['</body>', '</html>'])
    result = ''.join(contents)
    # remove empty paragraph
    result = str.replace(result, '<p style="text-align: left"></p>', '')
    return result


def parse_content(
        content: Union[Dict, List],
        contents: List[str],
        title: str,
        workdir: Path,
        ignore_paragraph: bool = False) -> None:
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
        contents.append(html_mapper.handle_image(content.get('attrs', {}), title, workdir, token, user))
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
    parser.add_argument('-t', '--token', nargs='?', help='Box access token')
    parser.add_argument('-o', '--output', nargs='?', help='Output file')
    parser.add_argument('-u', '--user', nargs='?', help='Box user id')
    args = parser.parse_args()
    workdir = Path(args.dir) if args.dir else Path.cwd()
    input_file = workdir / Path(args.input)
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    title = input_file.stem
    token = args.token if args.token else None
    user_id = args.user if args.user else None
    output_file = workdir / Path(args.output) if args.output else workdir / Path(f'{title}.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(parse(content, title, workdir, token, user_id))
