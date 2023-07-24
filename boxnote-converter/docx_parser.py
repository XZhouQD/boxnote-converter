"""
BoxNote to HTML Parser
Author: XZhouQD
Since: Jul 21 2023
"""
import argparse
from html_parser import parse
from pathlib import Path
from h2d import HtmlToDocx


def parse_docx(
        token: str,
        workdir: Path,
        input_file: Path,
        title: str,
        output_file: Path,
        output_docx: Path) -> None:
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(parse(content, title, workdir, token))
    docx_parser = HtmlToDocx(workdir)
    docx_parser.table_style = 'TableGrid'
    docx_parser.parse_html_file(output_file.absolute(), output_docx.absolute())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file name')
    parser.add_argument('-d', '--dir', help='Work directory')
    parser.add_argument('-t', '--token', nargs='?', help='Box access token')
    parser.add_argument('-o', '--output', nargs='?', help='Output file name')
    args = parser.parse_args()
    workdir = Path(args.dir) if args.dir else Path.cwd()
    input_file = workdir / Path(args.input)
    title = Path(input_file).stem
    output_file = workdir / Path(f'{title}.html')
    output_docx_file = Path(args.output) if args.output else Path(input_file.name)
    output_docx = workdir / output_docx_file
    token = args.token if args.token else None
    parse_docx(token, workdir, input_file, title, output_file, output_docx)
