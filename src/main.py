
import os
import json
import yaml
from features.blur import detect_blur
from features.color_texture import color_composition
from features.object_detection import detect_objects
from features.ocr import extract_text
from reasoning.llm_layer import llm_reasoning


def run_pipeline(img_path):
    config_path = os.path.join(os.path.dirname(__file__),"../config/settings.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"\n Starting Analysis for: {os.path.basename(img_path)}")
    print("-" * 50)

    print("[1/5] Checking for blur...")
    blur_sig = detect_blur(img_path, threshold=config['blur']['threshold'])

    print("[2/5] Analyzing color composition...")
    color_sig = color_composition(img_path, k=config['color']['clusters'])

    print("[3/5] Running object detection...")
    obj_sig = detect_objects(img_path)

    print("[4/5] Extracting text (OCR)...")
    ocr_sig = extract_text(img_path)

    visual_context = {
        "blur": blur_sig,
        "color": color_sig,
        "object": obj_sig,
        "ocr": ocr_sig
    }

    print("[5/5] Sending signals to Reasoning Layer...")

    API_KEY = os.getenv("GROQ_API_KEY")

    decision = llm_reasoning(visual_context, api_key=API_KEY)

    final_output = {
        "metadata": {
            "filename": os.path.basename(img_path),
            "system": "image-aware-reasoning-assistant"
        },
        "extracted_signals": visual_context,
        "final_decision": decision
    }

    return final_output



def run_batch_process(data_folder, output_folder):
   
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    image_files = [f for f in os.listdir(data_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png','.webp'))]
    
    print(f"Processing {len(image_files)} images from '{data_folder}'...")

    for filename in image_files:
        input_path = os.path.join(data_folder, filename)
       
        try:
            result = run_pipeline(input_path)
            name_only = os.path.splitext(filename)[0]
            output_filename = f"result_{name_only}.json"
            output_path = os.path.join(output_folder, output_filename)
            
            with open(output_path, "w") as f:
                json.dump(result, f, indent=4)
                
            print(f"Success: {filename} -> {output_filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "../data")
    OUTPUT_PATH = os.path.join(BASE_DIR, "../outputs")
    
    run_batch_process(DATA_PATH, OUTPUT_PATH)

