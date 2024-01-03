from facenet_pytorch import MTCNN
import torch
import cv2

image_facenet = cv2.imread("image.png")

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
detector = MTCNN(keep_all=True, device=device, post_process=False)

import numpy

bb, cc = detector.detect(torch.randn((224,224,3)).numpy())
cc

boxes, conf = detector.detect(image_facenet)
if conf[0] !=  None:
    for (x, y, w, h) in boxes:
        color = (0, 255, 255) 
        stroke = 3
        text = f"{conf[0]*100:.2f}%"
        x, y, w, h = int(x), int(y), int(w), int(h)
        cv2.putText(image_facenet, text, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 0), thickness=4)
        cv2.rectangle(image_facenet, (x, y), (w, h), color, stroke)

# box
# array([[1641.455322265625, 79.7732162475586, 1740.103271484375,
#         208.9061737060547],
#        [654.0436401367188, 135.28726196289062, 731.6705322265625,
#         218.16046142578125]], dtype=object)
        
import retinaface.RetinaFace
import PIL.Image
import numpy
import dlib
frame = numpy.array(PIL.Image.open('./002.png').convert("RGB"))
response = retinaface.RetinaFace.detect_faces(frame)
response['face_4']['facial_area']
response['face_4']['landmarks']['mouth_right'][0] - response['face_4']['landmarks']['mouth_left'][0]

def angle_between_points(point1, point2):
    import math
    x1, y1 = point1
    x2, y2 = point2
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return angle


def calculate_angle_between_vectors(u, v):
    dot_product = np.dot(u, v)
    magnitude_u = np.linalg.norm(u)
    magnitude_v = np.linalg.norm(v)

    cos_theta = dot_product / (magnitude_u * magnitude_v)

    # 使用反余弦函数计算角度（弧度）
    theta_radians = np.arccos(cos_theta)

    # 将弧度转换为角度
    theta_degrees = np.degrees(theta_radians)

    return theta_degrees

frame = numpy.array(PIL.Image.open('./03.png').convert("RGB"))
response = retinaface.RetinaFace.detect_faces(frame)
for item in response:
    face = response[item]
    u = np.array(face["landmarks"]["left_eye"]) - np.array(face["landmarks"]['nose'])
    v = np.array(face["landmarks"]["right_eye"]) - np.array(face["landmarks"]['nose'])
    angle = calculate_angle_between_vectors(u, v)
    print(angle)
    continue
    # left_eye = (face["landmarks"]["left_eye"][0], face["landmarks"]["left_eye"][1])
    # right_eye = (face["landmarks"]["right_eye"][0], face["landmarks"]["right_eye"][1])
    # # 计算两眼之间的角度
    # angle = angle_between_points(left_eye, right_eye)
    # print(angle)
    # # 根据角度判断人脸是正脸还是侧脸
    # if 30 < angle < 150:
    #     print("正臉")
    # else:
    #     print("側臉")

import numpy as np



import numpy
import facenet_pytorch
import PIL.Image
frame = numpy.array(PIL.Image.open("./002.png").convert("RGB"))

def getBox(frame, boundary, option=0):
    device = 'cuda' if(torch.cuda.is_available()) else 'cpu'
    model = facenet_pytorch.MTCNN(
        keep_all=True, 
        device=device, 
        post_process=False
    )
    height, width, _ = frame.shape
    area, confidence = model.detect(frame)
    if(confidence[0]==None or len(confidence)>1): return
    area = area.astype(int).flatten().tolist()
    if(boundary):
        scale = 1.0
        box = [
            max(0, area[0]-int((area[2]- area[0])*scale)),
            max(0, area[1]-int((area[3]- area[1])*scale)),
            min(width, area[2]+int((area[2]- area[0])*scale)),
            min(height, area[3]+int((area[3]- area[1])*scale))
        ]
        pass
    else: box = area
    return(box)









import PIL.Image
import numpy
import dlib
frame = numpy.array(PIL.Image.open('./001.png').convert("RGB"))
frame

predictor_path = "shape_predictor_68_face_landmarks.dat"  # 需要下载
predictor = dlib.shape_predictor(predictor_path)
