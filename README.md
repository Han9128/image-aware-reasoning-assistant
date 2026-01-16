
# Image-Aware Reasoning Assistant

An AI-powered pipeline designed to evaluate product images for professional e-commerce standards. This system combines **Computer Vision (TensorFlow/OpenCV)** with **Large Language Models (Groq/Llama-3)** to determine if an image is suitable for a high-end marketplace.



## Key Features
* **Multi-Stage Pipeline**: Decouples "Seeing" (Python/CV) from "Thinking" (LLM) for better accuracy and lower costs.
* **Blur Detection**: Mathematical analysis of image sharpness using Laplacian variance.
* **Object Recognition**: Deep Learning (MobileNetV2) to ensure the subject matches the product category.
* **Clean Background Check**: Dominant color coverage analysis via K-Means clustering.
* **OCR Integration**: Automated text extraction to identify prohibited watermarks or promotional text.
* **Structured Output**: Guaranteed JSON responses matching the requested project schema.

---

## Prerequisites
- Python 3.10.6 installed
- Git installed
- An LLM API key

## Installation & Setup

### 1. System Requirements
You must have **Tesseract OCR** installed on your system:
```bash
sudo apt update
sudo apt install tesseract-ocr
```
### 2. Clone the repository:
   ```bash
   git clone https://github.com/Han9128/Voice-bot.git
   cd Voice-bot
   ```

### 3. Python Environment
Create a virtual environment and install the required dependencies:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. API Configuration
- Create a `.env` file in the root directory.
- Add your GROQ AI API key inside:
```bash
GROQ_API_KEY=your_gsk_key_here
```

### 5. Run the application:
```bash
python src/main.py
```

### Output
The system generates a structured JSON report in outputs folder for every image processed, following this schema:

```
{
  "image_quality_score": 0.85,
  "issues_detected": ["minor background clutter"],
  "detected_objects": ["strawberry"],
  "text_detected": [],
  "llm_reasoning_summary": "The subject is clearly identified as a strawberry with high focus. The background has some variation but remains professional.",
  "final_verdict": "Suitable for professional e-commerce use",
  "confidence": 0.92
}
```

