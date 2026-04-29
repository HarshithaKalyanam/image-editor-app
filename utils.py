import numpy as np
from PIL import Image
import cv2

def pil_to_cv2(img):
    img = np.array(img)

    if img.shape[-1] == 4:  # PNG with transparency
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return img

def cv2_to_pil(img):
    if len(img.shape) == 2:
        return Image.fromarray(img)
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))