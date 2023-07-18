# Boxnote Converter

## Description
This is my own boxnote converter to (currently only) HTML.

This is suitable for the new format of BoxNotes after August 2022 (see [this issue](https://github.com/alexwennerberg/boxnotes2html/issues/3)).

## Usage
1. Clone this repo
1. Put the new boxnotes folder into your desired work directory
1. If you want the converter to download image automatically with only a `.boxnote` file, you need to pass a valid `box_access_token` to the tool
1. Run `python3 boxnote-converter/html_parser.py <example.boxnote> -d <work_dir> [-t] [box_access_token]` to convert to html
1. Or, run `python3 boxnote-converter/docx_parser.py <example.boxnote> -d <work_dir> [-t] [box_access_token]` to convert to docx (this will automatically create a html conversion in middle)
1. Check result at `example.html` or `example.docx` in `work_dir`

## Debug and Customize
1. Please check the current example files in `resource/` directory - the new boxnote should have a folder contains all their images called `Box Notes Images/` which have `<BoxNote Title> Images/` directory in it.
1. There is a predefined table css in `boxnote-converter/html_mapper.py`, feel free to edit it as you wish.

## Supported
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
 - Image (local)
 - Hyperlink
 - Block Quote
 - Divider Line (Horizontal Rule)
 - Code Block
 - Callout

## No support
 - File preview
 - Table of Contents (?)
