import cv2, numpy as np

def orb_streaming():
    VideoSignal = cv2.VideoCapture(0)
    set_w = 640
    set_h = 480

    while True:

        ret, frame = VideoSignal.read()
        frame = cv2.resize(frame,(set_w, set_h))
        #h, w, c = frame.shape
        ret  , buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        print("Streaming processing")
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame)+ b'\r\n')
