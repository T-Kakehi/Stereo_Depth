import numpy as np
import cv2
from matplotlib import pyplot as plt

# read images
imgL = cv2.imread('./images/unrealcv_desk_l.png',0)
imgR = cv2.imread('./images/unrealcv_desk_r.png',0)

plt.figure(figsize=(6,3))

stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
disparity_px_16 = stereo.compute(imgL, imgR)

fov = 90  # [deg]
B = 20  # [cm]
width = disparity_px_16.shape[1]  # [px]
fov_ = fov * np.pi / 180  # [rad]
ratio = (width/2) / np.tan(fov_/2)

depth = B * ratio * 16.0 / disparity_px_16

depth[np.where(depth < 0)] = 0
depth[np.where(depth > 400)] = 0

min_dst = 0
max_dst = 400

# # show result
plt.imshow(depth)
plt.colorbar()
plt.show()