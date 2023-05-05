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


def parse(boxnote_content: Union[str, bytes, bytearray], title: str) -> str:
    """
    Parse BoxNote to HTML
    """
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

    parse_content(boxnote.get('doc', {}).get('content', {}), contents)

    return '\n'.join(contents)


def parse_content(content: Union[Dict, List], contents: List[str], ignore_paragraph=False) -> None:
    """
    Parse BoxNote content
    """
    if not content:
        return

    if isinstance(content, list):
        for item in content:
            parse_content(item, contents, ignore_paragraph)
        return

    if not isinstance(content, dict):
        return

    if 'type' not in content:
        logger.error('Invalid BoxNote content: no type field')
        raise ValueError('Invalid BoxNote content: no type field')
    
    type_tag = content.get('type', '')
    if type_tag == 'paragraph':
        if not ignore_paragraph:
            contents.append(html_mapper.get_tag_open('paragraph'))
            parse_content(content.get('content', []), contents)
            contents.append(html_mapper.get_tag_close('paragraph'))
        else:
            parse_content(content.get('content', []), contents)
    elif type_tag == 'text':
        contents.append(html_mapper.get_tag_open('text'))
        contents.append(html_mapper.handle_text_marks(content.get('marks', []), content.get('text', '')))
        contents.append(html_mapper.get_tag_close('text'))
    elif type_tag == 'check_list_item':
        contents.append(html_mapper.get_tag_open('check_list_item', checked="checked" if content['attrs']['checked'] else ""))
        parse_content(content.get('content', []), contents, ignore_paragraph=True)
        contents.append(html_mapper.get_tag_close('check_list_item'))
    elif type_tag == 'image':
        contents.append(html_mapper.handle_image(content.get('attrs', {}), title))
    elif type_tag in ['strong', 'em', 'underline', 'strikethrough', 'ordered_list', 'bullet_list', 'list_item', "blockquote",
                      'check_list', 'table', 'table_row', 'table_cell', 'heading', 'link', 'font_size', 'font_color', "horizontal_rule"]:
        contents.append(html_mapper.get_tag_open(type_tag, **content.get('attrs', {})))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close(type_tag, **content.get('attrs', {})))
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        content = f.read()
    title = pathlib.Path(args.input).stem
    output_file = pathlib.Path(args.input).parent / pathlib.Path(f'{title}.html')
    with open(output_file, 'w') as f:
        f.write(parse(content, title))
