import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

angles_raw = ["0,3", "0,6", "0", "1,2", "1,5", "1,8", "2,1", "2,4", "2,7"]
#photos = [np.array(Image.open("haz("+angle+"grados).tif")) for angle in angles_raw]
photos = Image.open("haz(1,8grados).tiff")
photos.show()
#print(photos[0,:,:])
