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
    aveleavetime = Column(Float)
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
    diff = Column(Integer)
    linename = relationship("LineName", back_populates="lineque") 

meta = Base.metadata
meta.create_all(engine)




# Read an RGB image and return it in CHW format.
model = YOLOv3(n_fg_class=None,pretrained_model='voc0712')

print(voc_bbox_label_names[14])
idx_person = int(voc_bbox_label_names.index("person"))
print(idx_person)

# flask app
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
        .first()
    session.close()
    result = {
        "data":{
        "time":str(res_sort.ob_time),
        "count":str(res_sort.count),
        "que_time":str(res_sort.que_time)
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
    #print("labels", type(labels) , labels)
    #print(bboxes)
    
    for label, score in zip(labels[0],scores[0] ) :
        print(label, score)
    
    # count
    num_person =  np.sum(labels[0]==idx_person)

    # db用にデータを作成
    idd = key + str(time_posted)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 直前のn個のデータ
    res_pre = session.query(LineQue)\
        .filter(LineQue.device==key)\
        .order_by(desc(LineQue.ob_time))\
        .first()

    #直前のデータとの差分
    if res_pre is None:
        diff = 0 
    else:
        diff = num_person - res_pre.count
        diff_time = time_posted - res_pre.ob_time
    
    # 待ち時間を計算する
    res_ln = session.query(LineName)\
        .filter(LineName.device==key)\
        .first()

    que_time = num_person * float(res_ln.aveleavetime)
    print("\nque_time", que_time, "\n")
    # record
    record = LineQue(id=idd , device=key, ob_time=float(time_posted), 
                    count= int(num_person), diff=diff, que_time=que_time
                )
    print(record)
    session.add(record)
    
    # average leave time の計算
    row_count = session.query(LineQue).filter(LineQue.device==key).count()
    if row_count % 10==0:
        res_new_ave = session.query(LineQue)\
            .filter(LineQue.diff < 0).all() 
        su = 0 
        for re in res_new_ave:
            su -= re.diff
        print("sum", su)
        res_ln.aveleavetime = diff_time / float(su+ 0.000000001  / row_count) + 0.000000001
        session.add(res_ln)

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
    app.run(debug=False, port=8080)