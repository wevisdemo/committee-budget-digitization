"""
Document processing module for orchestrating the entire document extraction workflow.

This module contains the DocumentProcessor class that coordinates PDF processing,
schema management, and data extraction using the Gemini API.
"""

import os
from typing import Dict, Any, Optional
from .pdf_processor import PDFProcessor
from .schema_manager import SchemaManager
from .gemini_extractor import GeminiExtractor


class DocumentProcessor:
    """Main orchestrator class that coordinates PDF processing, schema management, and data extraction."""
    
    def __init__(self, api_key: str, model_name: str, schema_path: str):
        """
        Initialize the DocumentProcessor with all necessary components.
        
        Args:
            api_key: Google Gemini API key for authentication
            model_name: The Gemini model to use (e.g., "gemini-2.0-flash", "gemini-1.5-pro")
            schema_path: The path to the JSON file containing the schema for the output structure
        """
        self.gemini_extractor = GeminiExtractor(api_key, model_name)
        self.schema_manager = SchemaManager(schema_path)
        self.pdf_processor = PDFProcessor()
    
    def extract_data_from_all_pages(self, input_file_path: str) -> Optional[Dict[str, Any]]:
        """
        Extracts structured data from all pages of a PDF file using the Gemini API
        and returns it as a JSON object based on the provided schema.

        Args:
            input_file_path: The path to the input PDF file

        Returns:
            A dictionary containing the extracted data from all pages matching the provided schema,
            or None if extraction fails.
        """
        # Load the JSON schema
        if not self.schema_manager.load_schema():
            return None
        
        # Get the total number of pages in the PDF
        try:
            total_pages = self.pdf_processor.get_pdf_page_count(input_file_path)
            print(f"PDF has {total_pages} pages. Processing each page individually...")
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
        
        # Initialize the combined results
        combined_results = {"reports": []}
        
        # Process each page individually
        for page_num in range(total_pages):
            print(f"\n--- Processing Page {page_num + 1} of {total_pages} ---")
            
            # Extract the specific page
            temp_page_file = None
            try:
                temp_page_file = self.pdf_processor.extract_pdf_page(input_file_path, page_num)
                print(f"Extracted page {page_num + 1} to temporary file: {temp_page_file}")
                
                # Process this page
                page_result = self.gemini_extractor.extract_data_from_single_page(
                    input_file_path=temp_page_file,
                    schema_manager=self.schema_manager,
                    page_number=page_num
                )
                
                if page_result and "reports" in page_result:
                    # Add the reports from this page to the combined results
                    combined_results["reports"].extend(page_result["reports"])
                    print(f"Successfully processed page {page_num + 1}. Found {len(page_result['reports'])} report(s).")
                else:
                    print(f"Warning: No valid data extracted from page {page_num + 1}")
                    
            except Exception as e:
                print(f"Error processing page {page_num + 1}: {e}")
                continue
            finally:
                # Clean up temporary file
                if temp_page_file and os.path.exists(temp_page_file):
                    try:
                        os.unlink(temp_page_file)
                        print(f"Cleaned up temporary file: {temp_page_file}")
                    except Exception as e:
                        print(f"Warning: Failed to delete temporary file {temp_page_file}: {e}")
        
        print(f"\n--- Processing Complete ---")
        print(f"Total reports extracted: {len(combined_results['reports'])}")
        
        return combined_results if combined_results["reports"] else None
    
    def extract_data_from_single_page(self, input_file_path: str, page_number: int) -> Optional[Dict[str, Any]]:
        """
        Extracts structured data from a single page of a file using the Gemini API.
        
        Args:
            input_file_path: The path to the input file (PDF, image, etc.)
            page_number: The page number being processed (0-indexed)
            
        Returns:
            A dictionary containing the extracted data matching the provided schema,
            or None if extraction fails.
        """
        # Load the JSON schema
        if not self.schema_manager.load_schema():
            return None
        
        return self.gemini_extractor.extract_data_from_single_page(
            input_file_path=input_file_path,
            schema_manager=self.schema_manager,
            page_number=page_number
        )
