
import openai
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def llm_reasoning(visual_signals,api_key=None):

    if not api_key:
        print("\n[MOCK LLM] No API key found. Running heuristic reasoning...")
        
        blur_data = visual_signals.get('blur', {})
        color_data = visual_signals.get('color', {})
        obj_data = visual_signals.get('object', {})
        ocr_data = visual_signals.get('ocr', {})

        is_blurry = blur_data.get('is_blurry', False)
        
        
        is_cluttered = color_data.get('is_cluttered', False)
        has_text = ocr_data.get('has_text', False)
        subject = obj_data.get('primary_subject', 'unknown object')

        if is_blurry:
            verdict = False
            reason = f"Image is rejected because it is too blurry (Score: {visual_signals['blur']['blur_score']})."
        elif is_cluttered:
            verdict = False
            reason = "The background is too cluttered for a professional product shot."
        else:
            verdict = True
            reason = f"This is a high-quality image of a {subject} with a clean background and clear focus."

        return {
            "is_suitable": verdict,
            "quality_score": 40 if is_blurry else 95,
            "reasoning": reason,
            "mock_mode": True
        }
    
    prompt = f"""You are an AI Quality Assurance expert for a high-end e-commerce platform.
    Your task is to analyze technical signals from a product image and decide if it meets professional standards.

    VISUAL SIGNALS:
    - Subject: {visual_signals['object']['primary_subject']} (Confidence: {visual_signals['object']['detected_objects'][0]['confidence']})
    - Blur Score: {visual_signals['blur']['blur_score']} (Threshold: {visual_signals['blur']['threshold_used']}) (is_blurry:{visual_signals['blur']['is_blurry']})
    - Dominant Color Coverage: {visual_signals['color']['dominant_colors'][0]['coverage']*100}%
    - Text Found: "{visual_signals['ocr']['detected_text']}" (Word Count: {visual_signals['ocr']['word_count']})(has_text: {visual_signals['ocr']['has_text']})

    CRITERIA:
    1. Low blur scores (near or below threshold) indicate poor quality.
    2. Backgrounds should be clean (High dominant color coverage).
    3. No promotional text or watermarks are allowed in main listing photos.
    4. The subject must be clearly identified and relevant to e-commerce.
    5. Do not add anything extra from your side just give json what described in OUTPUT FORMAT below

    OUTPUT FORMAT:
    Return ONLY a valid JSON object. Do not include any other text or markdown fences.
    JSON SCHEMA:
    {{
      "image_quality_score": <float 0-1.0 based on clarity and composition>,
      "issues_detected": <list of strings highlighting defects like 'blur', 'clutter', or 'unwanted text'>,
      "detected_objects": <list of all objects identified in the image>,
      "text_detected": <list of specific words found by OCR>,
      "llm_reasoning_summary": <short paragraph explaining your logic>,
      "final_verdict": <string: "Suitable for professional e-commerce use" OR "Not suitable for professional e-commerce use">,
      "confidence": <float 0-1.0 representing your certainty in e-commerce use of the image>
    }}
              
    """
    
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1", 
        api_key=api_key
    )


    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {
                    "role": "user", 
                    "content": f"Analyze these image signals and return a JSON verdict: {json.dumps(visual_signals)}"
                }
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        print(f"Error calling Groq: {e}")
        return {"error": str(e)}

 



if __name__ == "__main__":
    # Mock data
    mock_signals = {
        "blur": {"blur_score": 1090.83, "threshold_used": 100},
        "color": {"dominant_colors": [{"coverage": 0.61}], "is_cluttered": False},
        "object": {"primary_subject": "strawberry", "detected_objects": [{"confidence": 0.99}]},
        "ocr": {"detected_text": "", "word_count": 0}
    }
    
    print(llm_reasoning(mock_signals))