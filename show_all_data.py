
import numpy as np
import cv2
import glob
import time
import json
if __name__ == "__main__":
    imgs = glob.glob('data/*.png')
    for each_img in imgs:
        each_json = each_img[:-4] + '.json'
        cv2.imread(each_img)
        with open(each_json, 'r', encoding='utf-8') as f:
            key = json.loads(f.read())
        print(key)
        cv2.imshow("Input", each_img)

        cv2.waitKey(0)