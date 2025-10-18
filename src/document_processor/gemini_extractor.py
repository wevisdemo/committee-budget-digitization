"""
Gemini API integration module for data extraction.

This module contains the GeminiExtractor class that handles interactions
with the Google Gemini API for extracting structured data from documents.
"""

import json
import pathlib
from typing import Dict, Any, Optional
from google import genai
from .schema_manager import SchemaManager


class GeminiExtractor:
    """Handles Gemini API interactions for data extraction."""
    
    def __init__(self, api_key: str, model_name: str):
        """
        Initialize the GeminiExtractor with API credentials.
        
        Args:
            api_key: Google Gemini API key for authentication
            model_name: The Gemini model to use (e.g., "gemini-2.0-flash", "gemini-1.5-pro")
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)
    
    def extract_data_from_single_page(
        self,
        input_file_path: str,
        schema_manager: SchemaManager,
        page_number: int
    ) -> Optional[Dict[str, Any]]:
        """
        Extracts structured data from a single page of a file using the Gemini API
        and returns it as a JSON object based on the provided schema.

        Args:
            input_file_path: The path to the input file (PDF, image, etc.)
            schema_manager: SchemaManager instance for prompt generation
            page_number: The page number being processed (0-indexed)

        Returns:
            A dictionary containing the extracted data matching the provided schema,
            or None if extraction fails.
        """
        # Get the filename for display
        display_name = pathlib.Path(input_file_path).name
        
        # Generate a generic prompt based on the schema structure
        prompt = schema_manager.generate_prompt(page_number + 1)  # +1 for human-readable page numbers
        
        print(f"Uploading file: {input_file_path}...")
        uploaded_file = None
        
        try:
            # Upload the file to the Gemini API using the new client format
            uploaded_file = self.client.files.upload(file=input_file_path)
            print(f"Completed upload: {uploaded_file}")

            print("Sending request to Gemini API...")
            # Make the API call to generate the content using the new client format
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    uploaded_file,
                    "\n\n",
                    prompt,
                ]
            )

            print("Successfully received response.")
            # Clean and parse the JSON response
            # The API returns a string, so we need to load it into a Python dict
            response_text = response.text.strip()
            
            # Remove any markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove ```
            
            response_text = response_text.strip()
            extracted_data = json.loads(response_text)

            return extracted_data

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            # Clean up by deleting the uploaded file from the server
            if uploaded_file is not None:
                try:
                    print(f"Deleting uploaded file: {uploaded_file}")
                    # Note: File deletion method may need to be updated based on the new API
                    # self.client.files.delete(uploaded_file)  # Uncomment if this method exists
                except Exception as e:
                    print(f"Warning: Failed to delete uploaded file: {e}")
