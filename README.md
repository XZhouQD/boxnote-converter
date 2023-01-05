# Boxnote Converter

## Description
This is my own boxnote converter to (currently only) HTML.

This is suitable for the new format of BoxNotes after August 2022 (see [this issue](https://github.com/alexwennerberg/boxnotes2html/issues/3)).

## Usage
1. Clone this repo
1. Put the new boxnotes folder into `resource/` directory or any directory you want
1. Run `python3 boxnote-converter/html_parser.py <path/to/your/file.boxnote>`
1. Check result at `path/to/your/file.html`

## Debug
1. Please check the current example files in `resoource/` directory - the new boxnote should have a folder contains all their images called `Box Notes Images/` which have `<BoxNote Title> Images/` diretories in it.
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
 - Image (local)
 - Hyperlink
 - Block Quote
 - Divider Line (Horizontal Rule)

## Not supported yet
 - Formatting
    - Alignment
 - Image (Box shared link)
 - File preview
 - Code Block
 - Table of Contents (?)
 - Callout
