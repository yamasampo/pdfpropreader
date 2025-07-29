
import os

from typing import List
from PyPDF2 import PdfMerger

def combine_pdfs(output_pdf_file: str, input_pdf_files: List[str], 
                #  verbose: bool = True
                 ):
    """Combines multiple PDF files to a single PDF file. 

    Parameters
    ----------
    input_pdf_files: List[str]
        A list of input PDF file paths. 
    output_pdf_file: str
        A path to an output PDF file. 
    """
    # Initialize the PdfMerger object
    merger = PdfMerger()
    print(f'{len(input_pdf_files)} input files are given.')
    # Iterate through the list of input PDF files
    for pdf in input_pdf_files:
        if os.path.exists(pdf):
            merger.append(pdf)
        else:
            raise FileNotFoundError(f"Input file {pdf} not found!")
    
    # Write the combined PDF to the output file
    merger.write(output_pdf_file)
    
    # Close the merger object
    merger.close()
    print(f"Combined PDF saved as {output_pdf_file}")

# Example usage
if __name__ == "__main__":
    # Get input arguments
    import sys
    # Output file path
    output_pdf_file = sys.argv[1]
    # List of PDF files to combine (replace with your file paths)
    input_pdf_files = sys.argv[2:]
    
    # Call the function to combine PDFs
    combine_pdfs(output_pdf_file, input_pdf_files)

