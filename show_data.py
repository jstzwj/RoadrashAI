
import numpy as np
import cv2
if __name__ == "__main__":
    data = np.load('data/raw_data-0.npy', allow_pickle=True)
    cv2.imshow("Input", data[0][0])
    cv2.waitKey(0)