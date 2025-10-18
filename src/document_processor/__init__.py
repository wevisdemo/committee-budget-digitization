"""
Document Processing Package

This package provides classes for processing PDF documents and extracting
structured data using the Google Gemini API.

Classes:
    PDFProcessor: Handles PDF file operations
    SchemaManager: Manages JSON schema and prompt generation
    GeminiExtractor: Handles Gemini API interactions
    DocumentProcessor: Main orchestrator for the entire workflow
"""

from .pdf_processor import PDFProcessor
from .schema_manager import SchemaManager
from .gemini_extractor import GeminiExtractor
from .document_processor import DocumentProcessor

__version__ = "1.0.0"
__author__ = "Boonjira Angsumalee"

__all__ = [
    "PDFProcessor",
    "SchemaManager", 
    "GeminiExtractor",
    "DocumentProcessor"
]
