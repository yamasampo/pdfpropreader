# pdfpropreader

Read properties of PDF files and combine PDF files. 

## Features

This package currently has two independent features. 

### 1. Extract properties and annotations from a PDF file

A Python script, `extract_pdf_property.py`, creates a plain text file that lists document information (a value returned by `PyPDF2.PdfFileReader().getDocumentInfo()`) and text annotations.

#### Usage

```shell
python3 extract_pdf_property.py [-a] input_pdf_file output_txt_file
```

#### Arguments

- input_pdf_file: A path to an input PDF file. 
- output_txt_file: A path to an output PDF file. 
- -a: Whether or not to include annotation text.

### 2. Combine multiple PDF files into a single file

A Python script, `combine_pdf_file.py`, creates a new PDF file by combining input PDF files in the given order. 

#### Usage

```shell
python3 combine_pdf_file.py output_file input_file_1 input_file_2 input_file_N
```

#### Arguments

- output_file: A path to an output PDF file. 
- input_file_1, input_file_2, ... input_file_N: N number of existing PDF files to be combined. If any of these files does not exist, this script raises a `FileNotFoundError`. 

## Dependency

- `PyPDF2` (confirmed on version 3.0.1)

