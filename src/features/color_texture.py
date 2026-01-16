import cv2
import numpy as np
from sklearn.cluster import KMeans

def color_composition(img_path, k = 3):
    
    image = cv2.imread(img_path)

    if image is None:
        raise ValueError(f"Can't open or find the image:{img_path}")
    
    image = cv2.resize(image,(100,100))
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    pixels = image.reshape(-1,3)

    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(pixels)
    colors = kmeans.cluster_centers_

    counts = np.bincount(labels)
    total = len(labels)

    analysis = []
    for i in range(k):
        analysis.append({
            "rgb": colors[i].astype(int).tolist(),
            "coverage": round(float(counts[i] / total), 2)
        })

    analysis = sorted(analysis, key=lambda x: x['coverage'], reverse=True)

    return {
        "dominant_colors": analysis,
        "is_cluttered": bool(analysis[0]['coverage'] < 0.5) 
    }


if __name__ == "__main__":

    res = color_composition("data/strawberry.jpeg")
    print(res)