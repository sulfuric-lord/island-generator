from PIL import Image
import numpy as np
h = np.load("heightmaps/frame_0180.npy")
img = Image.fromarray(h, mode="L")
img.save("frame_0180.png")