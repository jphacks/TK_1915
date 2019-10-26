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
    params = {"key":"kb3gbf8yg84gfbev"}
    response = requests.post(url, files=files, params= params)
    print(response.text)


def test_get_image(url):
    params = {"key":"kb3gbf8yg84gfbev"}
    response = requests.get(url, params=params)
    print(response.headers)
    print(response.url)
    #print(response.text)
    print(response.headers["content-type"])
    img = Image.open(io.BytesIO(response.content))
    img.show()

def test_get_count_key(url):
    params = {"key":"kb3gbf8yg84gfbev"}
    response = requests.get(url, params=params)
    print(response.headers)
    print(response.url)
    print(response.text)

def test_get_count_name(url):
    params = {"name":"本郷中央食堂"}
    response = requests.get(url, params=params)
    print(response.headers)
    print(response.url)
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
    test_get_count_key(url_count_k)

if __name__=="__main__":
    main()