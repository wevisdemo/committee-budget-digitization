"""
PDF processing module for handling PDF file operations.

This module contains the PDFProcessor class that handles PDF file operations
including page extraction and counting.
"""

import tempfile
import PyPDF2


class PDFProcessor:
    """Handles PDF file operations including page extraction and counting."""
    
    @staticmethod
    def extract_pdf_page(pdf_path: str, page_number: int) -> str:
        """
        Extracts a specific page from a PDF and saves it as a temporary file.
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number to extract (0-indexed)
            
        Returns:
            Path to the temporary file containing the extracted page
            
        Raises:
            ValueError: If the page number doesn't exist in the PDF
        """
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if page_number >= len(pdf_reader.pages):
                raise ValueError(f"Page {page_number} does not exist. PDF has {len(pdf_reader.pages)} pages.")
            
            # Create a new PDF with just the selected page
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_number])
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf_writer.write(temp_file)
            temp_file.close()
            
            return temp_file.name

    @staticmethod
    def get_pdf_page_count(pdf_path: str) -> int:
        """
        Gets the total number of pages in a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return len(pdf_reader.pages)
