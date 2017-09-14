import os
import cv2

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
        cx_new = float(cx) / w_img
        cy_new = float(cy) / h_img
        w_new = 1.8 * float(r2) / w_img
        h_new = 1.8 * float(r1) / h_img

        if (cx_new + w_new/2) > 1:
            w_new = 1.75 * (1 - cx_new)
        elif (cx_new - w_new/2) < 0:
            w_new = 1.75 * cx_new

        if (cy_new + h_new/2) > 1:
            h_new = 1.75 * (1 - cy_new)
        elif (cy_new - h_new/2) < 0:
            h_new = 1.75 * cy_new

        save_file.write('0' +                    # label 2 classes
                        " " + str(cx_new) +
                        " " + str(cy_new) +
                        " " + str(w_new) +
                        " " + str(h_new) + "\n")
        assert (cx_new + w_new/2 <= 1), ("cx_new + w_new/2 <= 1",
                                         name_list, cx_new + w_new/2)
        assert (cx_new - w_new/2 >= 0), ("cx_new - w_new/2 >= 0",
                                         name_list, cx_new - w_new/2)
        assert (cy_new + h_new/2 <= 1), ("cy_new + h_new/2 <= 1",
                                         name_list, cy_new + h_new/2)
        assert (cy_new - h_new/2 >= 0), ("cy_new - w_new/2 >= 0",
                                         name_list, cy_new - h_new/2)

        cx_draw = cx_new * w_img
        cy_draw = cy_new * h_img
        w_draw = w_new * w_img
        h_draw = h_new * h_img

        cv2.rectangle(img,
                      (round(cx_draw - w_draw / 2), round(cy_draw - h_draw/2)),
                      (round(cx_draw + w_draw / 2), round(cy_draw + h_draw/2)),
                      (0, 0, 255),
                      3)

        cv2.imwrite(str("%06d" % name_txt) +  '.png', img)

    save_file.close()






