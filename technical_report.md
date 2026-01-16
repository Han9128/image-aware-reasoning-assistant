# System Architecture

The image-aware reasoning assistant is designed as a modular pipeline where each component is responsible for a single concern. The system takes an image as input and produces a structured reasoning output by combining classical computer vision techniques with large language model (LLM) reasoning.

---

## Technical Pipeline Flow

The system is designed as a linear data-processing pipeline where each stage enriches the metadata until a final decision is reached.

### 1. Input & Preprocessing
The `main.py` orchestrator scans the `data/` directory. Images are validated for format (JPG, PNG. JPEG, Webp) and the image path is passed downstream to the concerned modules.

### 2. Feature Extraction Layer
The image is passed through four specialized detection modules.

**Signals Extracted:**

- **Blur Detection:** Calculates the Laplacian variance to measure edge sharpness.
- **Object Detection:** A MobileNetV2 model classifies the primary subject.
- **Color Analysis:** K-Means Clustering identifies dominant colors to detect background clutter.
- **OCR Extraction:** PyTesseract scans for any promotional text or watermarks.

### 3. Reasoning (LLM) Layer
The numerical "signals" from Stage 2 are serialized into a JSON string.  

This JSON is injected into a System Prompt that defines e-commerce quality standards.  

The Llama-3 (Groq) model interprets the data and generates a structured reasoning summary.

### 4. Orchestration & Output
The orchestrator receives the LLM's JSON response.  

The system combines the original metadata with the LLM’s analysis and saves a unique `.json` report into the `outputs/` folder.  

**Result:** A clean, scannable file ready for a marketplace's "Approve/Reject" dashboard.

---

## Why You Chose Your Approach

The goal of this project was not simply to classify images, but to build an explainable, scalable image-aware reasoning system that could realistically be used in a production environment such as an e-commerce platform. To achieve this, I deliberately chose a modular, grounded reasoning architecture that separates visual signal extraction from high-level decision-making.

### Modular Grounded Architecture
Rather than relying on a single end-to-end vision-language model, the system is designed as a pipeline of specialized components:

---

### Feature Extraction (`src/features/`)
The feature extraction layer is responsible for converting raw image data into objective, measurable visual signals. Each submodule focuses on a specific quality dimension that is relevant for professional image assessment.

#### Blur Detection (`blur.py`)
**Approach:** Laplacian variance

Blur detection is handled using Laplacian variance, a classical computer vision technique that measures edge strength. Sharp images contain strong high-frequency details, while blurry images produce low variance.  

It is objective, deterministic, extremely fast, and widely used in industry. The numeric blur score makes quality decisions explainable and easy to tune.

#### Color & Texture Analysis (`color_texture.py`)
**Approach:** K-Means clustering on RGB pixels  

Color distribution is used as a proxy for background cleanliness. Professional product images typically have one dominant background color, while cluttered images show fragmented color coverage.  

The module resizes the image, clusters pixel colors using K-Means, and measures dominant color coverage.  

It is lightweight, interpretable, and tunable. Dominant color coverage is easy to explain, inexpensive to compute, and effective for early-stage quality filtering.

#### Object Detection (`object_detection.py`)

**Approach:** MobileNetV2

MobileNetV2 was chosen to identify the primary subject of an image because it offers an effective balance between semantic accuracy and computational efficiency. It runs efficiently on CPU, requires no custom training, and provides fast inference suitable for real-time or large-scale batch processing. The model produces high-level object labels that serve as useful semantic signals for downstream LLM reasoning.

#### Optical Character Recognition (`ocr.py`)

**Approach:** Tesseract OCR with OpenCV preprocessing  

OCR is used to detect text such as watermarks or promotional overlays, which are common quality violations in product images. The pipeline converts images to grayscale, applies thresholding, and extracts text using Tesseract.  

Tesseract is a mature and reliable OCR engine that provides deterministic, explainable outputs. It is lightweight, fast, and well-suited for detecting short text without requiring large models.

---

### Reasoning Layer (`src/reasoning/`)
A Large Language Model is used only after visual signals are grounded in structured data. The LLM operates on compact JSON inputs rather than raw images, allowing it to focus on semantic reasoning and decision justification rather than visual perception.

#### LLM Reasoning Layer (`llm_layer.py`)
The LLM Reasoning layer analyzes structured visual signals (blur, color, object, OCR) to produce a final verdict on image suitability. It can run in mock heuristic mode or call an LLM API with a structured prompt.

**Llama-3 on Groq:**  
This model was chosen due to Groq’s extremely low inference latency as well as it being free. In an e-commerce workflow, sellers expect near-instant feedback when uploading images, and sub-second response times are critical for usability.

**Why this approach:**  
- **Explainable:** Decisions are based on objective signals, and the LLM provides human-readable reasoning.  
- **Efficient:** Only JSON data is sent to the LLM, reducing cost and latency.  

**Trade-offs:**  
- LLM reasoning may have subtle inconsistencies.  
- Raw image anomalies must be handled upstream by preprocessing.

**Why not end-to-end LLM vision model:**  
Direct image input is slower, costlier, and less interpretable. This hybrid approach balances deterministic features with flexible reasoning, making it production-ready.

---

### Orchestration (`src/main.py`)
The main entrypoint integrates all modules, ensuring clean data flow and consistent output formatting.  

This separation of concerns improves interpretability, testability, and extensibility. Each component can be independently improved or replaced without affecting the rest of the system.


## Limitations & Improvements

**Current Limitations:**

- **Feature coverage:** The system relies on basic visual signals (blur, color, object, OCR) and may miss more subtle quality issues such as lighting inconsistencies, reflections, or complex clutter.  
- **OCR & object constraints:** Tesseract struggles with stylized or low-contrast text, and MobileNetV2 uses generic ImageNet classes, which may not cover niche products.  
- **LLM reasoning variability:** Even with structured prompts, LLM outputs can sometimes be inconsistent or incomplete.  
 

**Potential Improvements:**

- Incorporate **semantic segmentation** or scene understanding for better clutter detection.  
- Upgrade to **domain-specific object detection models** for specialized product categories.  
- Use **OCR improvements** like layout-aware or deep-learning-based engines for complex text.  
- Add **feedback loop**: integrate user corrections to fine-tune thresholds and LLM reasoning.  
- Include **automated testing** and validation metrics for all modules to detect anomalies early.  

---

## Productionization

**Key Considerations:**

- **Modular deployment:** Each feature extraction module and the LLM layer can be containerized (e.g., Docker) for independent scaling.  
- **Batch & real-time processing:** Preprocessing and feature extraction can run in parallel for high-throughput pipelines; LLM reasoning can be called asynchronously to provide instant feedback.  
- **Monitoring & logging:** Track blur scores, OCR detections, object predictions, and LLM reasoning outputs for auditing and quality control.    

**Result:**  
A scalable, explainable, and cost-efficient pipeline ready to integrate into an e-commerce platform’s image approval workflow.

## Sample Outputs


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
