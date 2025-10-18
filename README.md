# Document Processor Package

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/yourusername/document-processor)

A professional Python package for extracting structured data from PDF documents using Google's Gemini API. The package processes PDFs page by page for better accuracy and allows you to define your desired output structure using JSON Schema.

## ✨ Features

- 🔄 **Page-by-Page Processing**: Processes PDFs page by page for better accuracy
- 📋 **Schema-Driven Extraction**: Define output structure using JSON Schema
- 📄 **PDF-Specific Optimization**: Optimized for multi-page PDF documents
- 🤖 **Automatic Prompt Generation**: Generates extraction prompts based on your schema
- 🇹🇭 **Thai Language Support**: Excellent support for Thai text extraction
- 📊 **JSON Output**: Returns structured data in JSON format matching your schema
- 🛡️ **Error Handling**: Robust error handling and resource cleanup
- 🗂️ **Temporary File Management**: Automatically manages temporary files during processing

## 📁 Project Structure

```

├── src/
│   └── document_processor/          # Main package
│       ├── __init__.py             # Package initialization
│       ├── pdf_processor.py        # PDF operations
│       ├── schema_manager.py       # JSON schema management
│       ├── gemini_extractor.py     # Gemini API integration
│       └── document_processor.py   # Main orchestrator
├── examples/
│   └── sample_data/                # Sample PDF files
│       └── test-2566.pdf           # Sample budget document
├── schema/
│   └── budget-schema.json          # Budget extraction schema
├── outputs/                        # Generated files
│   ├── output-raw.txt              # Raw extraction output
│   └── output.json                 # Formatted JSON output
├── main.py                         # Main execution script
├── requirements.txt                # Dependencies
└── README.md                      # This file
```

## 🚀 Installation


### Direct Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Get API Key

1. Get a Google Gemini API key:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create an API key
   - Add it to your environment or directly in the code

## 📖 Usage

### Basic Usage

```python
from src.document_processor import DocumentProcessor
import json

# Create processor instance
processor = DocumentProcessor(
    api_key="YOUR_API_KEY",
    model_name="gemini-2.0-flash",
    schema_path="schema/budget-schema.json"
)

# Extract data from all pages of a PDF
result = processor.extract_data_from_all_pages("examples/sample_data/test-2566.pdf")

if result:
    # Save results to files
    with open('outputs/output-raw.txt', 'w', encoding='utf-8') as f:
        f.write(str(result))
    
    with open('outputs/output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("Extraction completed! Check outputs/ directory for results.")
```

### Single Page Extraction

```python
from src.document_processor import DocumentProcessor

processor = DocumentProcessor(
    api_key="YOUR_API_KEY",
    model_name="gemini-2.0-flash",
    schema_path="schema/budget-schema.json"
)

# Extract data from a single page
result = processor.extract_data_from_single_page(
    input_file_path="examples/sample_data/test-2566.pdf",
    page_number=0  # 0-indexed
)
```

### Using Individual Components

```python
from src.document_processor import PDFProcessor, SchemaManager, GeminiExtractor

# Use PDF processor directly
pdf_processor = PDFProcessor()
page_count = pdf_processor.get_pdf_page_count("examples/sample_data/test-2566.pdf")

# Use schema manager
schema_manager = SchemaManager("schema/budget-schema.json")
prompt = schema_manager.generate_prompt(page_number=1)

# Use Gemini extractor
extractor = GeminiExtractor("api_key", "gemini-2.0-flash")
```

### Running the Main Script

The project includes a ready-to-use main script (`main.py`) that demonstrates the complete workflow:

```bash
# Make sure you have set your API key in main.py
# Edit the api_key variable in main.py with your Google Gemini API key

# Run the main script
python main.py
```

The script will:
1. Process the sample PDF (`examples/sample_data/test-2566.pdf`)
2. Extract structured data using the budget schema
3. Save results to `outputs/output-raw.txt` and `outputs/output.json`


## 📋 Requirements

- Python 3.8+
- google-generativeai==0.7.2
- PyPDF2>=3.0.0
- pytest>=7.4.0 (optional, for development)
- jupyter>=1.0.0 (optional, for development)
- See `requirements.txt` for complete list

## 🏗️ Development


### Project Architecture

The package follows a modular architecture with clear separation of concerns:

- **`PDFProcessor`**: Handles PDF file operations (extract pages, count pages)
- **`SchemaManager`**: Manages JSON schema loading and prompt generation
- **`GeminiExtractor`**: Handles Gemini API interactions
- **`DocumentProcessor`**: Main orchestrator that coordinates all components

## 📊 Example Schema

The project includes a budget-specific schema (`schema/budget-schema.json`) designed for extracting structured budget data:

```json
{
  "type": "object",
  "properties": {
    "reports": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "data_as_of": {"type": "string"},
          "table_data": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {"type": "string"},
                "rows": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "item": {"type": "string"},
                      "budget": {"type": "double"},
                      "disbursed": {"type": "double"},
                      "remaining": {"type": "double"}
                    },
                    "required": ["item", "budget", "disbursed", "remaining"]
                  }
                }
              },
              "required": ["category", "rows"]
            }
          },
          "total": {
            "type": "object",
            "properties": {
              "item": {"type": "string"},
              "budget": {"type": "double"},
              "disbursed": {"type": "double"},
              "remaining": {"type": "double"}
            },
            "required": ["item", "budget", "disbursed", "remaining"]
          }
        },
        "required": ["title", "data_as_of", "table_data", "total"]
      }
    }
  },
  "required": ["reports"]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


