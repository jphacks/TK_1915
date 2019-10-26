from flask import Flask, request, send_file, jsonify, make_response,  Response
from PIL import  Image
import io
from werkzeug.wsgi import FileWrapper
import json

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import Variable
from chainer.backends import cuda

import numpy as np
import pandas as pd

import os, sys, time
import pprint
import time
import urllib.error
import urllib.request
from PIL import Image
import io
import random, string
from chainercv.datasets import voc_bbox_label_names
from chainercv.links import YOLOv3
from chainercv.utils import read_image
from chainercv.visualizations import vis_bbox


app = Flask(__name__)

# Read an RGB image and return it in CHW format.
model = YOLOv3(n_fg_class=None,pretrained_model='voc0712')

print(voc_bbox_label_names[14])
idx_person = int(voc_bbox_label_names.index("person"))
print(idx_person)

app = Flask(__name__)

# limit upload file size : 2MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 2


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/image', methods=["get", "post"])
def image():
    img = request.files["file"].read()
    key=request.args.get('key')
    print("key", key)
    
    time_posted=time.time()
    
    # open by chainer 
    img = read_image(io.BytesIO(img))
 
    bboxes, labels, scores = model.predict([img])
    print("labels", type(labels) , labels)
    
    for label, score in zip(labels[0],scores[0] ) :
        print(label, score)
        
    # count
    num_person =  np.sum(labels[0]==idx_person)
    
    result = {
    "data": {
      "time":str(time_posted),
      "count": str(num_person)
      }
    }
    return jsonify(result) 



if __name__ == '__main__':
    app.run(debug=False, port=8080)