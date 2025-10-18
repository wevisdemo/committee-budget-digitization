"""
Schema management module for handling JSON schema operations.

This module contains the SchemaManager class that handles JSON schema loading
and prompt generation for the Gemini API.
"""

import json
from typing import Dict, Any, Optional


class SchemaManager:
    """Manages JSON schema loading and prompt generation."""
    
    def __init__(self, schema_path: str):
        """
        Initialize the SchemaManager with a schema file path.
        
        Args:
            schema_path: Path to the JSON schema file
        """
        self.schema_path = schema_path
        self._schema = None
    
    def load_schema(self) -> Optional[Dict[str, Any]]:
        """
        Load the JSON schema from file.
        
        Returns:
            The loaded schema dictionary or None if loading fails
        """
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as schema_file:
                self._schema = json.load(schema_file)
                return self._schema
        except Exception as e:
            print(f"Error loading JSON schema from {self.schema_path}: {e}")
            return None
    
    def get_schema(self) -> Optional[Dict[str, Any]]:
        """Get the loaded schema."""
        if self._schema is None:
            self.load_schema()
        return self._schema
    
    def generate_prompt(self, page_number: int = None) -> str:
        """
        Generates a generic prompt based on the JSON schema structure.
        
        Args:
            page_number: The page number being processed (optional)
            
        Returns:
            A generic prompt string that guides the model to extract data according to the schema
            
        Raises:
            ValueError: If schema is not loaded
        """
        schema = self.get_schema()
        if not schema:
            raise ValueError("Schema not loaded. Cannot generate prompt.")
        
        page_context = f" (Page {page_number})" if page_number else ""
        prompt_parts = [
            f"Please analyze this single page{page_context} of the document and extract structured data from it.",
            "\nThis page contains financial data. Please extract all relevant information from this specific page.",
            "\nExtract the data according to the following structure:\n"
        ]
        
        def describe_schema(obj: Any, indent: int = 0) -> str:
            """Recursively describes the schema structure."""
            description = ""
            prefix = "  " * indent
            
            if isinstance(obj, dict):
                obj_type = obj.get("type", "")
                
                if obj_type == "object":
                    properties = obj.get("properties", {})
                    required = obj.get("required", [])
                    
                    for prop_name, prop_schema in properties.items():
                        is_required = " (required)" if prop_name in required else " (optional)"
                        prop_type = prop_schema.get("type", "unknown")
                        
                        if prop_type == "array":
                            description += f"{prefix}- '{prop_name}'{is_required}: An array containing:\n"
                            items_schema = prop_schema.get("items", {})
                            description += describe_schema(items_schema, indent + 1)
                        elif prop_type == "object":
                            description += f"{prefix}- '{prop_name}'{is_required}: An object with:\n"
                            description += describe_schema(prop_schema, indent + 1)
                        else:
                            description += f"{prefix}- '{prop_name}'{is_required}: {prop_type}\n"
                            
                elif obj_type == "array":
                    items_schema = obj.get("items", {})
                    description += describe_schema(items_schema, indent)
                    
            return description
        
        schema_description = describe_schema(schema)
        prompt_parts.append(schema_description)
        prompt_parts.append(
            f"\nPlease extract all relevant information from this page{page_context} and return it in JSON format "
            "that strictly follows the provided schema. Ensure all required fields are included.\n\n"
            "CRITICAL: The 'reports' array should contain ONE entry for this specific page. "
            "If this page contains multiple sections, combine them into a single report entry.\n\n"
            "IMPORTANT: Return ONLY valid JSON without any markdown formatting, code blocks, or additional text. "
            "The response should be a valid JSON object that can be parsed directly."
        )
        
        return "".join(prompt_parts)
