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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer,ForeignKey, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import desc


engine = create_engine('sqlite:///db.sqlite3', echo=True)

Base = declarative_base()

class LineName(Base):
    """
    key と nameのマップ
    """
    __tablename__="linename"
    device=Column(String, primary_key=True)
    name=Column(String)
    lineque = relationship("LineQue", back_populates="linename")


class LineQue(Base):

    # テーブル名
    __tablename__ = 'lineque'
    # 個々のカラムを定義
    id = Column(String, primary_key=True)
    device = Column(String, ForeignKey('linename.device'))
    ob_time = Column(Float)
    count = Column(Integer)
    que_time = Column(Float)
    linename = relationship("LineName", back_populates="lineque") 

meta = Base.metadata
meta.create_all(engine)


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


@app.route("/count", methods=["get"])
def count():   
    name_query=request.args.get('name') 
    print("name=", name_query)
    Session = sessionmaker(bind=engine)
    session = Session()  
    res_sort = session.query(LineQue)\
        .join(LineName, LineQue.device==LineName.device)\
        .order_by(desc(LineQue.ob_time))\
        .limit(2).\
        all()
    print("\nres sort ", res_sort)
    session.close()
    result = {
        "data":{
        "time":str(res_sort[0].ob_time),
        "count":str(res_sort[0].count),
        "que_time":str(res_sort[0].que_time)
        }
    }
    return jsonify(result) 

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
    print(bboxes)
    
    for label, score in zip(labels[0],scores[0] ) :
        print(label, score)
    
    # count
    num_person =  np.sum(labels[0]==idx_person)

    # db用にデータを作成
    idd = key + str(time_posted)
    Session = sessionmaker(bind=engine)
    session = Session()  
    
    record = LineQue(id=idd , device=key, ob_time=float(time_posted), count= int(num_person))
    print(record)
    session.add(record)
    session.commit()
    session.close()
    
    result = {
    "data": {
      "time":str(time_posted),
      "count": str(num_person)
      }
    }
    return jsonify(result) 

if __name__ == '__main__':
    app.run(debug=True, port=8080)