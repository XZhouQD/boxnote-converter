# Boxnote Converter

## Description
This is my own boxnote converter to (currently only) HTML.

This is suitable for the new format of BoxNotes after August 2022 (see [this issue](https://github.com/alexwennerberg/boxnotes2html/issues/3)).

## Setup and Use
### Use in CLI
1. Clone this repo
1. Setup the repo using poetry:
```shell
python3 -m pip install poetry
poetry install
```
3. Put the new boxnotes folder into your desired work directory
1. If you want the converter to download image automatically with only a `.boxnote` file, you need to pass a valid `box_access_token` to the tool
1. Run `python3 boxnote-converter/html_parser.py <example.boxnote> -d <work_dir> [-t] [box_access_token]` to convert to html
1. Or, run `python3 boxnote-converter/docx_parser.py <example.boxnote> -d <work_dir> [-t] [box_access_token]` to convert to docx (this will automatically create a html conversion in middle)
1. Check result at `example.html` or `example.docx` in `work_dir`

### Use in coding
1. Use similar method as in CLI to setup
1. Use `docx_parser.parse_docx` or `html_parser.parse` to do the conversion.

## Debug and Customize
1. Please check the current example files in `example/` directory - the new boxnote should have a folder contains all their images called `Box Notes Images/` which have `<BoxNote Title> Images/` directory in it.
1. There is a predefined css in `boxnote-converter/html_mapper.py`, feel free to edit it as you wish.

### Supported Conversion
 - Text
 - Table
 - Headings
 - Ordered Lists
 - Unordered Lists
 - Checklists (by manual checkbox)
 - Formatting
    - Bold
    - Italic
    - Underline
    - Strikethrough
    - fort-size
    - font-color
    - highlight
    - alignment
 - Image
 - Hyperlink
 - Block Quote
 - Divider Line (Horizontal Rule)
 - Code Block
 - Callout

### No support
 - File preview
 - Table of Contents