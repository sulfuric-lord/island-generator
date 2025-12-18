from PIL import Image
import numpy as np
from scipy import ndimage
import os

INPUT_DIR = "rawframes"
OUTPUT_DIR = "heightmaps"
os.makedirs(OUTPUT_DIR, exist_ok=True)
files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".jpg"))


def load_bw(path, threshold=128):
    img = Image.open(path).convert("L")
    arr = np.array(img)
    bw = arr > threshold
    return bw

def compute_sdw(bw):
    inside = ndimage.distance_transform_edt(bw)
    outside = ndimage.distance_transform_edt(~bw)
    sdf = inside - outside
    return sdf

def sdf_to_height(sdf, power=0.7):
    h = np.clip(sdf, 0, None)
    if h.max() > 0:
        h /= h.max()
    h = h ** power
    return h

def smooth(height, sigma=1.2):
    return ndimage.gaussian_filter(height, sigma=sigma)

for i, fname in enumerate(files):
    path = os.path.join(INPUT_DIR, fname)
    bw = load_bw(path)
    sdf = compute_sdw(bw)
    height = sdf_to_height(sdf)
    height = smooth(height)
    height = (np.clip(height, 0, 1) * 255).astype(np.uint8)
    
    np.save(os.path.join(OUTPUT_DIR, f"frame_{i:04}.npy"), height)
    
    print(f"{i}/{len(files)} готово.")