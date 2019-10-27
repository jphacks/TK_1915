import sys
import time
import pprint
import time
import urllib.error
import urllib.request
import urllib.parse
import io
import random
import string
import json
import os

from flask import Flask, request, send_file, jsonify, make_response,  Response
from werkzeug.wsgi import FileWrapper

import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt

import chainer
import chainer.functions as F
from chainer import Variable
from chainer.backends import cuda

from chainercv.datasets import voc_bbox_label_names
from chainercv.links import YOLOv3
from chainercv.utils import read_image
from chainercv.visualizations import vis_bbox

filename = sys.argv[1]

# Read an RGB image and return it in CHW format.
model = YOLOv3(n_fg_class=None,pretrained_model='voc0712')

# open by chainer 
img = read_image(filename)
bboxes, labels, scores = model.predict([img])
#print("labels", type(labels) , labels)
#print(bboxes)


vis_bbox(img, bboxes[0], labels[0], scores[0],
        label_names=voc_bbox_label_names)
plt.show()