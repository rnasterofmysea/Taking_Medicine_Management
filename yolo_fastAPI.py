    
import cv2
import numpy as np
import requests
import sys
from selenium import webdriver
import urllib.request

from requests_toolbelt import MultipartEncoder
def yolo():
    ip = "http://192.168.0.6:8080"
    count = 0;
    #driver = webdriver.Chrome()
    #driver.get(ip+"/medicine/stream")
    
    #se = driver.find_element('xpath','//*[@id="video"]')
    #url = se.get_attribute('src')
    #test = urllib.request.urlopen(url)
    #print(test)
    #test2= test.read().decode("utf-8")

    # 웹캠 신호 받기
    VideoSignal = cv2.VideoCapture(0)
    #VideoSignal = cv2.VideoCapture(test2)
    set_w = 640
    set_h = 480
    # YOLO 가중치 파일과 CFG 파일 로드
    YOLO_net = cv2.dnn.readNet("yolov3_tiny_training_last.weights","yolov3_tiny_training.cfg")

    # YOLO NETWORK 재구성
    classes = []
    with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = YOLO_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]

    while True:
        # 웹캠 프레임
        #roi = None
        
        ret, frame = VideoSignal.read()
        frame = cv2.resize(frame,(set_w,set_h))
        h, w, c = frame.shape

        # YOLO 입력
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
        True, crop=False)
        YOLO_net.setInput(blob)
        outs = YOLO_net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:

            for detection in out:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    dw = int(detection[2] * w)
                    dh = int(detection[3] * h)
                    # Rectangle coordinate
                    x = int(center_x - dw / 2)
                    y = int(center_y - dh / 2)
                    boxes.append([x, y, dw, dh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    if confidence > 0.4:
                        count = count + 1
                        if count == 10:
                            roi = frame[y:y+dh, x:x+dw]
                            print(type(roi))
                            print(roi)
                            dir_path = "/home/sonnonet/darknet/yolov3_tiny/project/roi/"
                            file_path = "roi1.jpg"
                            ab_path = dir_path + file_path
                            cv2.imwrite(ab_path, roi)
                            files = open(ab_path, "rb")
                            field = {'check_img': files}
                            m = MultipartEncoder(fields=field)
                            headers = {'Content-Type': m.content_type}
                            print(m.content_type)
                            requests.post(ip+"/yolo/img/upload", files={"check_img":files})
                            print(type(VideoSignal))
                            VideoSignal = False 
                            # 
                            #break

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)


        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                score = str(confidences[i])

                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                cv2.putText(frame, label, (x, y + 10), cv2.FONT_ITALIC, 0.5, 
                (255, 255, 255), 1)
                cv2.putText(frame, score, (x, y + 20), cv2.FONT_ITALIC, 0.5,(255, 255, 255), 1)
                

        cv2.namedWindow('YOLOv3_tiny');
        cv2.resizeWindow(winname="YOLOv3", width=400, height=200)
        #cv2.imshow("YOLOv3_tiny", frame)

            
            #break
        #if cv2.waitKey(100) > 0:
            #break
        ret, buffer = cv2.imencode('.jpg', frame)
            # frame을 byte로 변경 후 특정 식??으로 변환 후에
            # yield로 하나씩 넘겨준다.
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame) + b'\r\n')
