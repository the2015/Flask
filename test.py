# Stubs for threading
import os
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor

import numpy as np

from create_arg import request_queue

try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

from json import JSONDecoder

import cv2
import face_recognition
import requests

from ext import socketio, lock

total_image_name = []
total_face_encoding = []
similarity = 0
test = None
face_detector = cv2.CascadeClassifier(
    "E:\PYTHON3.7\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")  # 级联检测器获取文件

compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
key = "SASuuvcBxQmaweSsUH06xeV3ouCdjrLU"
secret = "JP6XgFiqH7zMZSh0nUh0LngyYg8Fe0UQ"
val = {
    "name": "",
    "value": 0
}
filepath = "D:\\mypro\\pycharworkspace\\Flask\\"  # 模型数据图片目录os.listdir(os.path.abspath("../"))
for fn in os.listdir(filepath + "img\\face_recognition"):  # fn 表示的是文件名q
    total_face_encoding.append(
        face_recognition.face_encodings(
            face_recognition.load_image_file(filepath + "img\\face_recognition\\" + fn))[0])
    fn = fn[:(len(fn) - 4)]  # 截取图片名（这里应该把images文件中的图片名命名为为人物名）
    total_image_name.append(fn)  # 图片名字列表

executor = ThreadPoolExecutor(max_workers=2)


def drawFace(face_rectangle, img):
    width = face_rectangle['width']
    top = face_rectangle['top']
    left = face_rectangle['left']
    height = face_rectangle['height']
    start = (left, top)
    end = (left + width, top + height)
    color = (55, 255, 155)
    thickness = 3
    cv2.rectangle(img, start, end, color, thickness)


def save_pricame():
    w_size = []
    for i in range(1, 11):
        fn = filepath + "img\\face_recognition\\yyf.jpg"
        # print 'load %s as ...' % fn
        img = cv2.imread(fn)
        sp = img.shape
        # print sp
        sz1 = sp[0]  # height(rows) of image
        sz2 = sp[1]  # width(colums) of image
        sz3 = sp[2]  # the pixels value is made up of three primary colors
        # print 'width: %d \nheight: %d \nnumber: %d' % (sz1, sz2, sz3)
        w_size.append(sz2)
    a = w_size
    b = max(w_size)
    c = a.index(b)
    c += 1
    return c


def print_time():
    print(_threading.current_thread())
    # faceId2 = filepath + "img\\test\\model.jpg"
    # data = {"api_key": key, "api_secret": secret}
    # res = 0
    # for name in total_image_name:
    #     faceId1 = filepath + "img\\face_recognition\\" + name + ".jpg"  # 原图模型
    #     files = {"image_file1": open(faceId1, "rb"), "image_file2": open(faceId2, "rb")}
    #     response = requests.post(compare_url, data=data, files=files)
    #     req_con = response.content.decode('utf-8')
    #     req_dict = JSONDecoder().decode(req_con)
    #     confindence = req_dict['confidence']
    #     if confindence > res:
    #         val = {
    #             "name": name,
    #             "value": confindence,
    #         }
    #     if val.get("value") > 60:
    #         img1 = cv2.imread(faceId2, 0).copy()
    #         cv2.imwrite(filepath + "img/result/" + name + ".jpg", img1)
    #         print("比对值:" + str(confindence))
    #         socketio.emit('my_response',
    #                       {'data': "姓名：" + name + "识别值：" + str(confindence)},
    #                       namespace='/test')
    #     else:
    #         socketio.emit('my_response',
    #                       {'data': "无法识别"},
    #                       namespace='/test')


# image = request_queue.get()
# _threading.Thread(target=custom).start()
# if task2.done():
#     task1 = executor.submit(custom)


def custom(image):
    start = time.time()
    # print(_threading.current_thread())
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings):
        # 看看面部是否与已知人脸相匹配。
        for i, v in enumerate(total_face_encoding):
            match = face_recognition.compare_faces(
                [v], face_encoding, tolerance=0.5)
            # print(face_distances1, "--------")
            name = "Unknown"
            if match[0]:
                name = total_image_name[i]
                face_distances = face_recognition.face_distance([total_face_encoding[i]], face_encoding)
                print(name)
                print(face_distances)
                break
    print('完成时间', time.time() - start)
    lock.release()
# _threading.Thread(target=custom).start()
