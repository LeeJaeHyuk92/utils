import os
import cv2
import numpy as np


# parameter to be modified
debug = False
thresh_min = 120
thresh_max = 121


path_img = 'images'
name_img = 'example.png'
img = cv2.imread(os.path.join(path_img, name_img), cv2.IMREAD_GRAYSCALE)


for thresh in range(thresh_min, thresh_max + 1, 1):
    _, img_bin = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    img_value = img == thresh
    img_value = img_value.astype(np.uint8)
    np.place(img_value, img_value > 0, 255)

    if debug:
        cv2.imshow("threshold", img_bin)
        cv2.imshow("only_" + str(thresh) + "value", img_value)
        cv2.waitKey(0)

    cv2.imwrite(path_img + '/' + str(thresh) + '_threshold_' + str(name_img),
                img_bin)
    cv2.imwrite(path_img + '/' + str(thresh) + '_value' + str(name_img),
                img_value)
