import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os

MODEL = MobileNetV2(weights='imagenet')

def detect_objects(img_path,k=3):

    img = image.load_img(img_path, target_size=(224,224))

    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    x = preprocess_input(x)

    predictions = MODEL.predict(x,verbose=0)

    decoded = decode_predictions(predictions,top=k)[0]

    results = []

    for _, label,score in decoded:
        results.append({
            "label":label.replace("_"," "),
            "confidence":round(float(score),3)
        })
    
    return {
        "detected_objects":results,
        "primary_subject": results[0]["label"] if results else "unknown"
    }


if __name__ == "__main__":
    img_path = "data/strawberry.jpeg"
    try:
        res = detect_objects(img_path)
        print(res)
    except Exception as e:
        print(f"Error during detection: {e}")