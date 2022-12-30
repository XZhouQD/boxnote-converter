'''
BoxNote to HTML Parser
Author: XZhouQD
Since: Dec 30 2022
'''

import json
from typing import Dict, List, Union
import logging
from logging import Logger
import mapper.html_mapper as html_mapper


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format = log_format, level=logging.INFO)
logger = logging.getLogger()


def parse(boxnote_content: Union[str, bytes, bytearray], title: str) -> str:
    '''
    Parse BoxNote to HTML
    '''
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
    '''
    Parse BoxNote content
    '''
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
    if type_tag == 'paragraph' and not ignore_paragraph:
        logger.info('paragraph')
        contents.append(html_mapper.get_tag_open('paragraph'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('paragraph'))
    elif type_tag == 'paragraph' and ignore_paragraph:
        logger.info('paragraph ignore')
        parse_content(content.get('content', []), contents)
    elif type_tag == 'text':
        logger.info('text')
        contents.append(html_mapper.get_tag_open('text'))
        contents.append(html_mapper.handle_text_marks(content.get('marks', []), content.get('text', '')))
        contents.append(html_mapper.get_tag_close('text'))
    elif type_tag == 'strong':
        logger.info('strong')
        contents.append(html_mapper.get_tag_open('strong'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('strong'))
    elif type_tag == 'em':
        logger.info('em')
        contents.append(html_mapper.get_tag_open('em'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('em'))
    elif type_tag == 'underline':
        logger.info('underline')
        contents.append(html_mapper.get_tag_open('underline'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('underline'))
    elif type_tag == 'strikethrough':
        logger.info('strikethrough')
        contents.append(html_mapper.get_tag_open('strikethrough'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('strikethrough'))
    elif type_tag == 'font_size':
        logger.info('font_size')
        contents.append(html_mapper.get_tag_open('font_size', **content.get('attrs', {}).get('size', '')))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('font_size'))
    elif type_tag == 'font_color':
        logger.info('font_color')
        contents.append(html_mapper.get_tag_open('font_color', **content.get('attrs', {}).get('color', '')))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('font_color'))
    elif type_tag == 'ordered_list':
        logger.info('ordered_list')
        contents.append(html_mapper.get_tag_open('ordered_list'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('ordered_list'))
    elif type_tag == 'bullet_list':
        logger.info('bullet_list')
        contents.append(html_mapper.get_tag_open('bullet_list'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('bullet_list'))
    elif type_tag == 'list_item':
        logger.info('list_item')
        contents.append(html_mapper.get_tag_open('list_item'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('list_item'))
    elif type_tag == 'check_list':
        logger.info('check_list')
        contents.append(html_mapper.get_tag_open('check_list'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('check_list'))
    elif type_tag == 'check_list_item':
        logger.info('check_list_item')
        if content['attrs']['checked']:
            contents.append(html_mapper.get_tag_open('check_list_item_checked'))
        else:
            contents.append(html_mapper.get_tag_open('check_list_item'))
        parse_content(content.get('content', []), contents, ignore_paragraph=True)
        contents.append(html_mapper.get_tag_close('check_list_item'))
    elif type_tag == 'table':
        logger.info('table')
        contents.append(html_mapper.get_tag_open('table'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('table'))
    elif type_tag == 'table_row':
        logger.info('table_row')
        contents.append(html_mapper.get_tag_open('table_row'))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('table_row'))
    elif type_tag == 'table_cell':
        logger.info('table_cell')
        contents.append(html_mapper.get_tag_open('table_cell', **content.get('attrs', {})))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('table_cell'))
    elif type_tag == 'heading':
        logger.info('heading')
        contents.append(html_mapper.get_tag_open('heading', **content.get('attrs', {})))
        parse_content(content.get('content', []), contents)
        contents.append(html_mapper.get_tag_close('heading',  **content.get('attrs', {})))
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('output', help='Output file')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        content = f.read()
    with open(args.output, 'w') as f:
        f.write(parse(content, args.input.split('/')[-1].split('.')[0]))
