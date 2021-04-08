import os
from PyPDF2 import PdfFileReader
from collections import namedtuple

PDFinfo = namedtuple(
    'PDFinfo', 
    ['file_path', 'properties', 'annotations']
)

def main(input_pdf_file, output_txt_file, include_annotations=True):
    """ Extracts properties of PDF file contents and outputs the extracted 
    properties to a text file. 

    Parameters
    ----------
    input_pdf_file: str
        A path to a PDF file of which properties are extracted. 
    output_txt_file: str
        A path to an output file. If output file already exists, this program 
        raises FileExists error. 

    Return
    ------
    pdf_property: PDFproperty (namedtuple)
        A namedtuple object for PDF properties. Currently, five fields of title, 
        author, subject, keywords and metadata are available.

    """
    check_output_file_not_exist(output_txt_file)
    pdf_info = read_pdf_file(input_pdf_file, include_annotations)
    save_as_file(pdf_info, output_txt_file)

    return pdf_info

def check_output_file_not_exist(output_txt_file):
    """ Check if an output file does not exist. If exists, raises 
    FileExistsError. """
    if os.path.isfile(output_txt_file):
        raise FileExistsError(f'Output file "{output_txt_file}" already exists.')

def read_pdf_file(file_path, include_annotations=True):
    """ Returns contents of a given PDF file as a Python string object. 
    
    Parameter
    ---------
    file_path: str
        A path to a PDF file of which properties are extracted. 

    Reference
    ---------
    - PyPDF2 website: https://pythonhosted.org/PyPDF2
    """

    with open(file_path, 'rb') as f:
        # Initialize PdfFileReader object. 
        pdf = PdfFileReader(f)

        # Get PyPDF2.pdf.DocumentInformation object.
        # This has to be within "with" block, which means pdf.getDocumentInfo 
        # still accesses the filehandle "f"
        info = pdf.getDocumentInfo() 
        # This instance is similar to a dictionary but values are immutable.
        # Example for Mayo and Burger 1995 
        # {
        #     '/ModDate': 'D:20090216042737Z',
        #     '/Producer': 'PDFlib PLOP 3.0 (.NET/Win32)/PDFlib PLOP 2.1.0p1 (SunOS)/Acrobat Distiller 2.1 for Windows',
        #     '/Title': 'THE EVOLUTION OF DOMINANCE: A THEORY WHOSE TIME HAS PASSED?',
        #     '/WPS-ARTICLEDOI': '10.1111/j.1469-185X.1997.tb00011.x',
        #     '/WPS-PROCLEVEL': '2',
        #     '/Author': 'OLIVER MAYO and REINHARD BURGER',
        #     '/Subject': 'Biological Reviews of the Cambridge Philosophical Society',
        #     '/Keywords': 'Evolution; dominance; metabolic control theory; mimicry; industrial melanism',
        #     '/CreationDate': 'D:19970812183011'
        # }
        # The website saids the function tries to read five attributes of author, 
        # creator (this does not appear above because its value is None, meaning 
        # not read from the given PDF file), producer, subject. I am not sure how 
        # the program reads other fields like "ModDate" and "WPS-ARTICLEDOI". 
        # There may be a full list of fields internally.

        # Get annotation text
        if include_annotations:
            page_num = pdf.getNumPages()
            annotations = []
            keys = ['/Type', '/Subtype', '/CreationDate']

            for i in range(page_num):
                page = pdf.getPage(i)
                if '/Annots' in page:
                    for annot in page['/Annots']:
                        obj = annot.getObject()
                        if 'text' in obj['/Subtype'].lower():
                            annotations.append(
                                {k: obj[k] for k in keys + ['/Contents']}
                            )
                        else:
                            annotations.append(
                                {k: obj[k] for k in keys}
                            )
        else:
            annotations = []

    return PDFinfo(file_path, info, annotations)

def save_as_file(pdf_info, output_txt_file):
    """ Output PDF property as a plain text file. """
    property_lines = [
        f'{k} = {v}'
        for k, v in pdf_info.properties.items()
    ]
    annotation_lines = [
        f'\nAnnotation {n}:\n' +
        '\n'.join([f'{k} = {v}'for k, v in annot.items()])
        for n, annot in enumerate(pdf_info.annotations, 1)
    ]

    output_lines = \
        'property_num: {}\n'.format(len(property_lines)) + \
        '\n'.join(property_lines) + \
        '\n\nannotation_num: {}\n'.format(len(pdf_info.annotations)) + \
        '\n'.join(annotation_lines)

    with open(output_txt_file, 'w') as f:
        print('PDF_file_path = {}\n'.format(pdf_info.file_path), file=f)
        print(output_lines, file=f)

    return output_txt_file

def extract_property(contents, fields):
    """ Returns PDF property for given fields by reading through the entire 
    contents. Currently, this function is not used. PDF property is extracted
    by functions in PyPDF2 package.
    """
    pass

if __name__ == '__main__':
    import argparse
    desc = 'pdfpropreader: Extract properties of a PDF file content.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "input_input_pdf_file", 
        help="A path to an input PDF file"
    )
    parser.add_argument(
        "output_txt_file", 
        help="A path to an output file."
    )
    parser.add_argument(
        "-a", "--include_annotations", 
        help='Include annotation text in an output file if the flag '\
             '"-a" or "--include_annotations" is called.', 
        action="store_true"
    )

    args = parser.parse_args()
    main(
        args.input_input_pdf_file, args.output_txt_file, 
        args.include_annotations
    )
