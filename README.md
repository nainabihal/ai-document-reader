# Document AI System for Field Extraction from Invoices

This system extracts key fields from invoice documents (specifically tractor loan quotations) using OCR and heuristic-based field detection. It handles diverse document formats including scanned, digital, and multilingual invoices.

## Architecture Overview

The system follows a modular pipeline architecture:

```
Document Input (PDF/Image)
        ↓
    Preprocessing
        ↓
       OCR Layer
        ↓
   Field Extraction
        ↓
Structured JSON Output
```

### Components

1. **Document Ingestion**: Converts PDFs to images using pdf2image, handles both PDF and image inputs.
2. **OCR Processing**: Uses PaddleOCR for text recognition with support for multiple languages.
3. **Field Detection**: Regex-based extraction for text fields, keyword-based detection for visual elements.
4. **Post-Processing**: Confidence scoring, validation, and output formatting.

## Pipeline Details

### 1. Document Ingestion and Interpretation
- Input: PDF or image files
- PDF conversion: pdf2image library converts each page to high-quality images
- Image processing: Direct processing for PNG/JPG files

### 2. Visual and Textual Understanding
- OCR: PaddleOCR extracts text with bounding boxes and confidence scores
- Multi-page support: Processes all pages in multi-page PDFs
- Language support: English with orientation detection

### 3. Field Detection and Entity Recognition
- **Dealer Name**: Regex pattern matching "dealer", "seller", "vendor" followed by name
- **Model Name**: Pattern matching "model" or "tractor" followed by model identifier
- **Horse Power**: Numeric extraction with "HP" suffix
- **Asset Cost**: Currency pattern matching with digit extraction
- **Signature/Stamp**: Keyword-based detection with placeholder bounding boxes

### 4. Semantic Reasoning and Structuring
- Fuzzy matching for dealer names (heuristic-based)
- Exact matching for model, HP, and cost
- Binary presence detection for visual elements

### 5. Post-Processing and Quality Assurance
- Confidence calculation based on field completeness
- Processing time tracking
- Cost estimation (placeholder based on cloud inference)

## Cost and Latency Analysis

### Estimated Performance
- **Latency**: ~3-8 seconds per document (depending on document complexity)
- **Cost**: $0.002 per document (based on CPU/GPU inference costs)
- **Accuracy Target**: ≥95% Document-Level Accuracy (DLA)

### Cost Breakdown
- OCR Processing: ~$0.001 (PaddleOCR inference)
- Image Processing: ~$0.0005 (OpenCV operations)
- Field Extraction: ~$0.0005 (Regex and heuristics)

### Scalability Considerations
- Batch processing support for multiple documents
- Modular design allows for GPU acceleration
- Low-cost open-source components (PaddleOCR, OpenCV)

## Handling Lack of Ground Truth

Since no labeled data is provided, the system uses:

1. **Heuristic Rules**: Regex patterns and keyword matching for field extraction
2. **Pseudo-Labeling**: Automatic label generation based on extraction confidence
3. **Self-Consistency**: Multiple extraction attempts with consensus voting

## Installation and Usage

### Installation
```bash
pip install -r requirements.txt
```

### Usage

#### Web UI (Recommended)
```bash
streamlit run app.py
```
This launches a web interface where you can upload documents and see results instantly.

#### Command Line

##### Single Document
```bash
python executable.py --input path/to/document.pdf --output result.json
```

##### Batch Processing
```bash
python executable.py --input path/to/documents/ --output results/ --batch
```

### Output Format
```json
{
  "doc_id": "invoice_001",
  "fields": {
    "dealer_name": "ABC Tractors Pvt Ltd",
    "model_name": "Mahindra 575 DI",
    "horse_power": 50,
    "asset_cost": 525000,
    "signature": {"present": true, "bbox": [100, 200, 300, 250]},
    "stamp": {"present": true, "bbox": [400, 500, 500, 550]}
  },
  "confidence": 0.96,
  "processing_time_sec": 3.8,
  "cost_estimate_usd": 0.002
}
```

## Evaluation Metrics

- **Document-Level Accuracy (DLA)**: Percentage of documents with all 6 fields correctly extracted
- **Field-level mAP**: Mean Average Precision for signature/stamp detection
- **Latency**: Average processing time per document
- **Cost**: Estimated inference cost per document

## Future Improvements

1. **Advanced Visual Detection**: Implement YOLO or similar for accurate signature/stamp detection
2. **VLMs Integration**: Use Qwen2.5-VL for better layout understanding
3. **Multilingual Support**: Enhanced OCR for Hindi/Gujarati text
4. **Active Learning**: Incorporate human feedback for iterative improvement

## Dependencies

- paddlepaddle: Deep learning framework for OCR
- paddleocr: OCR engine
- opencv-python: Image processing
- pdf2image: PDF to image conversion
- Pillow: Image handling
- numpy: Numerical operations
