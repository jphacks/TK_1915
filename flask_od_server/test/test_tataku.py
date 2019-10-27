"python test_tataku.py <url>"

import json
import requests
from PIL import Image
import io
import sys

def test_hello(url):
    response = requests.get(url)
    print(response.headers)
    print(response.url)
    print(response.text)
    print(response.headers["content-type"])

def test_post_image(url, key):

    files = {"file":("P95jirou.jpg.png", open("image/P95jirou.jpg", "rb"), "image/P95jirou.jpg"),
            }
    params = {"key":key}
    response = requests.post(url, files=files, params= params)
    print(response.text)


def test_get_count_name(url, name):
    params = {"name":str(name)}
    response = requests.get(url, params=params)
    print(response.headers)
    print("url", response.url)
    print(response.text)


def main():
    url_base = sys.argv[1]
    url_hello = url_base + "/"
    test_hello(url_hello)
    print("\n\npost images")
    url_image= url_base +"/image"
    for key in ["sjcohfvy39y223cfdsa", "wfdiskgwhfn2y811211", "w0903eihcnteffazba", "u98ny22skahgcntfoem"]:
        test_post_image(url_image, key)
    print("\n\nget count")
    url_count_k = url_base + "/count"
    print("\n")
    for name in ["本郷中央食堂", "本郷第二食堂", "銀杏メトロ食堂", "カフェテリア若葉"]:
        print(name)
        test_get_count_name(url_count_k, name)
        print("\n")

    


if __name__=="__main__":
    main()