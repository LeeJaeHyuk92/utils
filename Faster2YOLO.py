import cv2
import os
import re


def main():
    path = os.getcwd()
    data_path = os.path.join(path, "ImageSets/all.txt")
    anno_path = os.path.join(path, "Annotations/")
    img_path = os.path.join(path, "Images/")

    f = open(data_path, 'r')
    lines = f.readlines()
    names = [x.strip() for x in lines]

    for name in names:
        save_file = open(str(name + '.txt'), 'w')
        filename = str(anno_path + name + '.txt')
        jpgname = str(img_path + name + '.jpg')
        img = cv2.imread(jpgname)
        h_img, w_img, _ = img.shape

        temp_f = open(filename, 'r')
        temp_lines = temp_f.readlines()
        temp_names = [x.strip() for x in temp_lines]

        label = 0

        # annotation ...
        for temp_name in temp_names:
            try:
                objs = re.findall('\\(\\d+, \\d+\\)[\\s\\-]+\\(\\d+, \\d+\\)',
                              temp_name)
            except:
                continue

        for idx, obj in enumerate(objs):
            coor = re.findall('\\d+', obj)

            x_l = float(coor[0])
            y_l = float(coor[1])
            x_r = float(coor[2])
            y_r = float(coor[3])

            cx = (x_l + x_r) / 2
            cy = (y_l + y_r) / 2
            w = x_r - x_l
            h = y_r - y_l

            cx = cx / w_img
            cy = cy / h_img
            w = w / w_img
            h = h / h_img

            save_file.write(str(0) + ' ' +
                            str(cx) + ' ' +
                            str(cy) + ' ' +
                            str(w) + ' ' +
                            str(h) + '\n')

        save_file.close()

if __name__ == '__main__':
    main()