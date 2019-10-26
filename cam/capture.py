import cv2
import requests
import sys
import io
import hashlib
import time

def create_hash_from_date(date):
    hash = hashlib.sha1()
    hash.update(date)
    return hash.hexdigest()[:10]

def image_to_byte_array(image):
    _, encoded_image = cv2.imencode('.png', image)
    return encoded_image.tobytes()

def get_img_from_cam(cam_id=1):
    cap = cv2.VideoCapture(cam_id)
    _, frame = cap.read()
    frame = cv2.resize(frame, (frame.shape[1], frame.shape[0]))

    cv2.imshow('Raw Frame', frame)

    k = cv2.waitKey()
    cap.release()
    cv2.destroyAllWindows()

    return image_to_byte_array(frame)

def main():
    url = sys.argv[1]
    img = get_img_from_cam()
    timestamp = str(time.time())
    files = {"file":(timestamp + ".png", img),}
    params = {"key":create_hash_from_date(timestamp.encode('utf-8'))}
    response = requests.post(url, files=files, params= params)
    return response.text

if __name__ == '__main__':
    main()
