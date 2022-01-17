import numpy as np
import cv2
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import matplotlib.cm as cm
import csv

DISPARTIES = 50

MIN_DST = 0
MAX_DST = 400

cell_size = 5
cell_size2 = 10

NOISE_RATIO = 1

def clean_noise(img, height_diff, width_diff, reheight, rewidth):
    lw = 0
    w = 0
    while w <= rewidth+DISPARTIES*2:
        w += width_diff
        lh = 0
        h = 0
        while h <= reheight*2:
            h += height_diff
            # print(w, h)
            if height_diff*width_diff*765*NOISE_RATIO >= np.sum(img[lh : h,lw : w]):
                img[lh : h,lw : w] = [0, 0, 0]
            lh = h
        lw = w
    return img

# read images
imgL = cv2.imread('./images/unrealcv_desk_l.png',0)
imgR = cv2.imread('./images/unrealcv_desk_r.png',0)
height,width = imgL.shape[:2]
print(width, height)

# plt.figure(figsize=(6,3))
stereo = cv2.StereoSGBM_create(numDisparities = DISPARTIES,blockSize = 9,mode = cv2.STEREO_SGBM_MODE_HH)
disparity_px_16 = stereo.compute(imgL, imgR)
fov = 90  # [deg]
B = 20  # [cm]
width = disparity_px_16.shape[1]  # [px]
fov_ = fov * np.pi / 180  # [rad]
ratio = (width/2) / np.tan(fov_/2)
depth = B * ratio * 16.0 / disparity_px_16
depth[np.where(depth < MIN_DST)] = 0
depth[np.where(depth > MAX_DST)] = 0
# np.savetxt('np_savetxt_5e.txt', depth, fmt='%d')

# show result
# plt.imshow(depth)
# plt.colorbar()
# plt.show()
# cv2.imshow('depth.png', depth)

print(depth.shape)
img = np.zeros((height, width, 3))
img[np.where(depth > 0)] = [255, 255, 255]
resize = img[0:height, 50:width]
rewidth,reheight = resize.shape[:2]

NOISE_RATIO = 0.7
clean_img_1 = clean_noise(resize, 5, 10, reheight, rewidth)
clean_img_2 = clean_noise(clean_img_1, 10, 5, reheight, rewidth)
NOISE_RATIO = 0.6
clean_img = clean_noise(clean_img_2, 10, 10, reheight, rewidth)
# cv2.imshow('clean_img.png',clean_img)

w = 0
x = list(range(0))
y = list(range(0))
z = list(range(0))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
while w < rewidth:
        h = 0
        while h < reheight:
            if clean_img[w,h][0] == 255:
                if not (depth[w,h] == 0):
                    x.append(h)
                    y.append(rewidth-w)
                    z.append(int(depth[w,h]))
                    # print(w,h,depth[w,h])
            h += 1
        w += 1

# print("What a name of output file?")
# file_name = input()
file_name = "full"

f = open(str(file_name+'.csv'), 'w', newline='')
data = [x,y,z]
writer = csv.writer(f)
writer.writerows(data)
f.close()

ax.view_init(elev=270, azim=90)
ax.scatter(x,y,z,c=z,cmap='jet')
plt.show()

# cv2.imshow('disparity', clean_img)
# cv2.waitKey(0)