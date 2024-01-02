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
response = retinaface.RetinaFace.detect_faces(image_facenet)
response


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