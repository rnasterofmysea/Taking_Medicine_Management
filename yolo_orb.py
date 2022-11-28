import cv2, numpy as np
import requests
import sys
from requests_toolbelt import MultipartEncoder
import base64

def image_data():
    ip = "http://192.168.0.6:8080"
    parameter = "/orb/img"
    res = requests.post(ip + parameter, headers = {'Content-Type': 'application/json'})
    res = res.content.decode('utf-8')
    image_list = res.split(',')
    return image_list

def feature_matching(query_img, test_img, index):
    print("::: type query_image")
    print(type(query_img))
    gray1 = cv2.cvtColor(query_img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(desc1, desc2)

    # 매칭 결과를 거리기준 오름차순으로 정렬 ---③
    matches = sorted(matches, key=lambda x:x.distance)
    # 모든 매칭점 그리기 ---④
    #res1 = cv2.drawMatches(query_img, kp1, test_img, kp2, matches, None, \
                            #flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    # 매칭점으로 원근 변환 및 영역 표시 ---⑤
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ])
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ])
        
    # RANSAC으로 변환 행렬 근사 계산 ---⑥
    mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    h,w = query_img.shape[:2]
    pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
    dst = cv2.perspectiveTransform(pts,mtrx)

    # 정상치 매칭만 그리기 ---⑦
    matchesMask = mask.ravel().tolist()
    # 모든 매칭점과 정상치 비율 ---⑧
    accuracy=float(mask.sum()) / mask.size
    if accuracy > 0.5:
            image_name = image_name_list[i]
            res = requests.get(ip+"/orb/recognitionJet?result="+image_name)

def orb():

    def image_data():
        ip = "http://192.168.0.6:8080"
        parameter = "/orb/img"
        res = requests.post(ip + parameter, headers = {'Content-Type': 'application/json'})
        res = res.content.decode('utf-8')
        image_list = res.split(',')
        print(image_list)
        return image_list

    def feature_matching(query_img, test_img, index):
        gray1 = cv2.cvtColor(query_img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        kp1, desc1 = detector.detectAndCompute(gray1, None)
        kp2, desc2 = detector.detectAndCompute(gray2, None)
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(desc1, desc2)

        # 매칭 결과를 거리기준 오름차순으로 정렬 ---③
        matches = sorted(matches, key=lambda x:x.distance)
     
        #매칭점으로 원근 변환 및 영역 표시 ---⑤
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ])
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ])
        
        # RANSAC으로 변환 행렬 근사 계산 ---⑥
        mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h,w = query_img.shape[:2]
        pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
        dst = cv2.perspectiveTransform(pts,mtrx)
        #test_img = cv2.polylines(test_img,[np.int32(dst)],True,255,3, cv2.LINE_AA)

        # 정상치 매칭만 그리기 ---⑦
        matchesMask = mask.ravel().tolist()
        # 모든 매칭점과 정상치 비율 ---⑧
        accuracy=float(mask.sum()) / mask.size
        print("accuracy: %d/%d(%.2f%%)"% (mask.sum(), mask.size, accuracy))
        if accuracy > 0.5:
                image_name = image_name_list[index]
                res = requests.get(ip+"/orb/recognitionJet?result="+image_name) 
    
    ip = "http://192.168.0.6:8080"
    image_download_parameter = '/orb/api/download/'
    image_name_list = image_data()
    print("::: image_name_list")
    print(image_name_list)
    print('::: image_name_list_len')
    print(len(image_name_list))
    detector = cv2.ORB_create()
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    #query_img = image_data
    #cv2.imwrite("./testest.jpg",query_img)
    VideoSignal = cv2.VideoCapture(0)
    set_w = 640
    set_h = 480
    accuracy_count = 0

    result_list=[]
    
    while True:
        
        ret, frame = VideoSignal.read()
        frame = cv2.resize(frame,(set_w, set_h))
        h,w,c = frame.shape
        test_image = frame
        i = 0
        #while i < len(image_name_list):
        while i < 2:
            print("::: How to request")
            print(ip + image_download_parameter + image_name_list[i])
            res = requests.post(ip + image_download_parameter + image_name_list[i], headers = {'Content-Type':'image/jpeg'})
            encoded_img = np.fromstring(res.content, dtype=np.uint8)
            query_image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
            feature_matching(query_image,test_image,i)
            i = i + 1
        ret  , buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        print("Streaming processing")
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame)+ b'\r\n')

