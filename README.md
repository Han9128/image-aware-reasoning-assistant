
# Image-Aware Reasoning Assistant

An AI-powered pipeline designed to evaluate product images for professional e-commerce standards. This system combines **Computer Vision (TensorFlow/OpenCV)** with **Large Language Models (Groq/Llama-3)** to determine if an image is suitable for a professional website.


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
   git clone https://github.com/Han9128/image-aware-reasoning-assistant.git
   cd image-aware-reasoning-assistant
   ```

### 3. Python Environment
Create a virtual environment and install the required dependencies:
```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. API Configuration
- Create a `.env` file in the root directory.
- Add your GROQ API key inside:
```bash
GROQ_API_KEY=your_gsk_key_here
```

### 5. Run the application:
```bash
python src/main.py
```

### Output
The system generates a structured JSON report in outputs folder for every image processed, following this schema:

```json
{
    "metadata": {
        "filename": "blur_strawberry.png",
        "system": "image-aware-reasoning-assistant"
    },
    "extracted_signals": {
        "blur": {
            "is_blurry": true,
            "blur_score": 10.13,
            "threshold_used": 100.0
        },
        "color": {
            "dominant_colors": [
                { "rgb": [60, 91, 22], "coverage": 0.6 },
                { "rgb": [202, 212, 216], "coverage": 0.24 },
                { "rgb": [172, 70, 60], "coverage": 0.16 }
            ],
            "is_cluttered": false
        },
        "object": {
            "detected_objects": [
                {"label": "mitten", "confidence": 0.196},
                {"label": "strawberry", "confidence": 0.141},
                {"label": "thimble", "confidence": 0.078}
            ],
            "primary_subject": "mitten"
        },
        "ocr": {
            "detected_text": "",
            "word_count": 0,
            "has_text": false
        }
    },
    "final_decision": {
        "image_quality_score": 0.2,
        "issues_detected": ["blur"],
        "detected_objects": ["mitten", "strawberry", "thimble"],
        "text_detected": [],
        "llm_reasoning_summary": "The image is blurry with a low blur score, which indicates poor quality. Although the background is not cluttered and there's no promotional text, the subject is not clearly identified with low confidence. The dominant color coverage is 60%, which is relatively high but not sufficient to outweigh the blur issue.",
        "final_verdict": "Not suitable for professional e-commerce use",
        "confidence": 0.6
    }
}
```

