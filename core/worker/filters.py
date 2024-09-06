from PIL import Image
import numpy as np
from skimage.filters import threshold_otsu

def crop_blank_spaces(image):
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image)
    thresh = threshold_otsu(img_array)
    binary = img_array < thresh

    rows = np.any(binary, axis=1)
    cols = np.any(binary, axis=0)
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    
    padding = 10
    ymin = max(0, ymin - padding)
    ymax = min(img_array.shape[0], ymax + padding)
    xmin = max(0, xmin - padding)
    xmax = min(img_array.shape[1], xmax + padding)
    cropped = image.crop((xmin, ymin, xmax, ymax))
    return cropped
