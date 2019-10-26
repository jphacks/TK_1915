import sys
import io
import hashlib
import time
import typing

import cv2
import requests
from numpy import ndarray


def create_hash_from_date(date: str) -> str:
    '''
      create unique (ASAP) hash from date string
      args:
        str date: date string
      ret:
        str hased date string
    '''
    hash = hashlib.sha1()
    hash.update(date)
    return hash.hexdigest()[:10]

def image_to_byte_array(image: ndarray) -> bytes:
    '''
      encode ndarray image to byte string
      args:
        ndarray: image
      ret:
        bytes: image encoded as byte string
    '''
    _, encoded_image = cv2.imencode('.png', image)
    return encoded_image.tobytes()

def get_img_from_cam(cap: cv2.VideoCapture) -> ndarray:
    '''
      capture and edit camera image
      args:
        cv2.VideoCapture cap: captured source
      ret:
        ndarray: edited image
    '''
    _, frame = cap.read()
    frame = cv2.resize(frame, (frame.shape[1], frame.shape[0]))
    cv2.imshow('Raw Frame', frame)
    return frame

def main():
    # capture interval as mili seconds
    interval = 10000
    base_url = sys.argv[1]
    post_url = base_url + '/image'
    cam_id = 1
    cap = cv2.VideoCapture(cam_id)
    while True:
    # hesitate to use while loop
        img = get_img_from_cam(cap)
        k = cv2.waitKey(interval)
        if k == 27:#ESC
            break
    else:
        cap.release()
        cv2.destroyAllWindows()

    timestamp = str(time.time())
    byte_img = image_to_byte_array(img)
    files = { "file": (timestamp + ".png", byte_img) }
    params = { "key":create_hash_from_date(timestamp.encode('utf-8')) }
    response = requests.post(post_url, files=files, params= params)
    return response

if __name__ == '__main__':
    response = main()
    try:
        print(response.text)
    except Exception as e:
        print(e)
