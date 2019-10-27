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

def test_post_image(url):

    files = {"file":("P95jirou.jpg.png", open("image/P95jirou.jpg", "rb"), "image/P95jirou.jpg"),
            }
    params = {"key":"sjcohfvy39y223cfdsa"}
    response = requests.post(url, files=files, params= params)
    print(response.text)


def test_get_count_name(url):
    params = {"name":"本郷中央食堂"}
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
    test_post_image(url_image)
    print("\n\nget count")
    url_count_k = url_base + "/count"
    test_get_count_name(url_count_k)

    print("\n\npost images")
    url_image= url_base +"/image"
    for i in range(102):
        print("tataku i~",i)
        test_post_image(url_image)


if __name__=="__main__":
    main()