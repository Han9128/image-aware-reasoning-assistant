
import cv2

def detect_blur(img_path,threshold=100.0):

    print("FILE:", __file__)
    image = cv2.imread(img_path)

    if image is None:
        raise ValueError(f"Can't open or find the image: {img_path}")

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    variance = cv2.Laplacian(gray,cv2.CV_64F).var()

    is_blurry = variance<threshold

    return {
        "is_blurry": bool(is_blurry),
        "blur_score": round(float(variance), 2),
        "threshold_used": threshold
    }


if __name__ == "__main__":
    res = detect_blur("data/strawberry.jpeg")
    print(res)