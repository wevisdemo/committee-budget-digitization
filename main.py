"""
Main script for document processing using the modular document processing package.

This script demonstrates how to use the DocumentProcessor class to extract
structured data from PDF documents using the Google Gemini API.
"""

import json
import pathlib
from src.document_processor import DocumentProcessor


# --- Script Execution ---
if __name__ == "__main__":
    # Example usage of the DocumentProcessor class
    
    # IMPORTANT: Set your Google API key here
    api_key = 'API_KEY'
    if not api_key:
        raise ValueError("Please set your Google API key in the api_key variable.")
    
    # Define the model to use
    model_name = "gemini-2.0-flash"
    
    # The name of the PDF file you want to process
    pdf_filename = "examples/sample_data/test-2566.pdf"
    pdf_path = pathlib.Path(pdf_filename)
    
    if not pdf_path.is_file():
        print(f"Error: The file '{pdf_filename}' was not found in the current directory.")
        print("Please make sure the PDF file is placed in the same folder as this script.")
    else:
        # Path to the JSON schema file
        schema_path = pathlib.Path("schema/budget-schema.json")
        
        if not schema_path.is_file():
            print(f"Error: The schema file 'budget-schema.json' was not found in the current directory.")
            print("Please make sure the budget-schema.json file is placed in the same folder as this script.")
        else:
            # Create the DocumentProcessor instance
            processor = DocumentProcessor(
                api_key=api_key,
                model_name=model_name,
                schema_path=str(schema_path)
            )
            
            # Process the PDF file
            json_output = processor.extract_data_from_all_pages(str(pdf_path))

            # Save the results
            with open('outputs/output-raw.txt', 'w', encoding='utf-8') as f:
                f.write(str(json_output))

            with open('outputs/output.json', 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)