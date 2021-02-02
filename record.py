
import os
import argparse
import time
import json
import random
import numpy as np
import cv2
import mss
import winsound
from pynput import keyboard

duration = 1000  # millisecond
do_freq = 440  # Hz
so_freq = 392 * 2
width = 640
height = 480

# up, down, left, right, x, a, s, z, d, alt
cur_key_vec = [0,0,0,0,0, 0,0,0,0,0]
is_exit = False
def on_press(key):
    if key == keyboard.Key.esc:
        is_exit = True
        print('exit key listener')
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    
    if k == 'up':
        cur_key_vec[0] = 1
    elif k == 'down':
        cur_key_vec[1] = 1
    elif k == 'left':
        cur_key_vec[2] = 1
    elif k == 'right':
        cur_key_vec[3] = 1
    elif k == 'x':
        cur_key_vec[4] = 1
    elif k == 'a':
        cur_key_vec[5] = 1
    elif k == 's':
        cur_key_vec[6] = 1
    elif k == 'z':
        cur_key_vec[7] = 1
    elif k == 'd':
        cur_key_vec[8] = 1
    elif k == 'alt':
        cur_key_vec[9] = 1

def on_release(key):
    if key == keyboard.Key.esc:
        is_exit = True
        print('exit key listener')
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    
    if k == 'up':
        cur_key_vec[0] = 0
    elif k == 'down':
        cur_key_vec[1] = 0
    elif k == 'left':
        cur_key_vec[2] = 0
    elif k == 'right':
        cur_key_vec[3] = 0
    elif k == 'x':
        cur_key_vec[4] = 0
    elif k == 'a':
        cur_key_vec[5] = 0
    elif k == 's':
        cur_key_vec[6] = 0
    elif k == 'z':
        cur_key_vec[7] = 0
    elif k == 'd':
        cur_key_vec[8] = 0
    elif k == 'alt':
        cur_key_vec[9] = 0

def collect(data_dir, index):
    for i in list(range(5))[::-1]:
        print(i)
        time.sleep(1)

    if not os.path.exists(data_dir):
        print('create the dir')
        os.makedirs(data_dir)
    else:
        print('continue collect')
    
    last_time = time.time()
    while(True):
        if is_exit:
            break

        with mss.mss() as sct:
            grab_mon_index = 0
            mon = sct.monitors[grab_mon_index]
            monitor = {
                "top": mon["top"] + 80,
                "left": mon["left"] + 0,
                "width": width,
                "height": height,
                "mon": grab_mon_index,
            }
            image = np.array(sct.grab(monitor))
            image = np.flip(image[:, :, :3], 2)
            image = image[:, :, ::-1]
        
        key = cur_key_vec
        
        img_file_name = os.path.join(data_dir, 'raw_img-{}.png'.format(index))
        json_file_name = os.path.join(data_dir, 'raw_json-{}.json'.format(index))
        cv2.imwrite(img_file_name, image)
        with open(json_file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(key))
        # show fps
        new_time = time.time()
        if index % 10 == 0:
            print('fps:{}'.format(1/(new_time-last_time)))
        index += 1
        last_time = time.time()

        time.sleep(0.1)
        
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data collect arguements.')

    parser.add_argument("-i", "--index", help="start number of data collect", type=int, default=0)
    parser.add_argument("-p", "--path", help="path of data collect", type=str, default='./data')

    args = parser.parse_args()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # start to listen on a separate threads
    collect(args.path, args.index)