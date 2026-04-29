import cv2
import numpy as np

def apply_blur(img, ksize):
    if ksize < 3:
        return img

    if ksize % 2 == 0:
        ksize += 1

    return cv2.GaussianBlur(img, (ksize, ksize), 0)

def apply_sharpness(img, alpha):
    if alpha <= 0:
        return img

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])

    sharp = cv2.filter2D(img, -1, kernel)
    return cv2.addWeighted(img, 1 - alpha, sharp, alpha, 0)

def adjust_brightness(img, beta):
    return cv2.convertScaleAbs(img, alpha=1, beta=beta)

def adjust_contrast(img, alpha):
    alpha = max(0.5, alpha)
    return cv2.convertScaleAbs(img, alpha=alpha, beta=0)

def edge_detection(img, t1, t2):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(img, t1, t2)

def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_img = cv2.transform(img, kernel)
    return np.clip(sepia_img, 0, 255).astype(np.uint8)


def cartoon(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 9, 9
    )
    color = cv2.bilateralFilter(img, 9, 300, 300)
    return cv2.bitwise_and(color, color, mask=edges)