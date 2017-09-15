import os
import cv2
import math

path = os.getcwd()
print(path)

anno_path = os.path.join(path, 'FDDB-all-EllipseList.txt')
f = open(anno_path, 'r')
lines = f.readlines()
names = [x.strip() for x in lines]

list_path = os.path.join(path, "FDDB-all.txt")
f_list = open(list_path, 'r')
lines_list = f_list.readlines()
names_list = [x.strip() for x in lines_list]
name_txt = 0
print('done')

for name_list in names_list:
    name_txt += 1
    img = cv2.imread(name_list)
    h_img, w_img, _ = img.shape
    name_list = name_list.replace('.jpg', '')

    save_file = open(str("%06d" % name_txt) + '.txt', 'w')
    idx = int(names.index(name_list))
    nums = int(names[idx + 1])
    for num in range(nums):
        name = names[idx + 2 + num].split(' ')
        r1, r2, angle, cx, cy, _ = name[:-1]
        cx_new = int(float(cx))
        cy_new = int(float(cy))
        w_new = int(1.8 * float(r2))
        h_new = int(1.8 * float(r1))

        # for SSD
        x_min = cx_new - math.floor(w_new / 2)
        y_min = cy_new - math.floor(h_new / 2)

        if (cx_new + w_new/2) > w_img:
            w_new = 1.75 * (w_img - cx_new)
        elif x_min < 0:
            w_new = 1.75 * cx_new

        if (cy_new + h_new/2) > h_img:
            h_new = 1.75 * (h_img - cy_new)
        elif y_min < 0:
            h_new = 1.75 * cy_new

        x_min = cx_new - math.floor(w_new / 2)
        y_min = cy_new - math.floor(h_new / 2)
        w_new = int(w_new)
        h_new = int(h_new)

        assert (cx_new + w_new/2 <= w_img), ("cx_new + w_new/2 <= 1",
                                         name_list, cx_new + w_new/2)
        assert (x_min >= 0), ("x_min >= 0",
                                         name_list, x_min)
        assert (cy_new + h_new/2 <= h_img), ("cy_new + h_new/2 <= 1",
                                         name_list, cy_new + h_new/2)
        assert (y_min >= 0), ("y_min >= 0",
                                         name_list, y_min)
        assert(0 <= w_new <= w_img), ("w_img: ", w_img, "w_new", w_new)
        assert (0 <= h_new <= h_img), ("h_img: ", h_img, "h_new", h_new)


        save_file.write('0' +                    # label 2 classes
                        " " + str(x_min) +
                        " " + str(y_min) +
                        " " + str(w_new) +
                        " " + str(h_new) + "\n")

        cv2.imwrite(str("%06d" % name_txt) + '.png', img)
        cv2.rectangle(img,
                      (x_min, y_min),
                      (x_min + w_new, y_min + h_new),
                      (0, 0, 255),
                      3)
        cv2.imwrite(str("gt_"+"%06d" % name_txt) + '.png', img)

    save_file.close()






