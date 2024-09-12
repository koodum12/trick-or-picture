import cv2
import mediapipe as mp # 구글에서 불러온 mediapipe 라이브러리 불러오기
import sys 
import filter,picture 
import numpy as np
import math
import asyncio

image_width = 640              
image_height = 480 
count = int(0)
#mp_drawing = mp.solutions.drawing_utils #랜드마크 표시
#mp_drawing_styles =mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) 
mp_face_mesh = mp.solutions.face_mesh

filter_number = int(input("안경 골라"))
filter_image_path = filter.checknumber(filter_number)

frame_number = int(input("필터 프레임 골라"))
frame_image_path = filter.frame_filter(frame_number)

people_number = int(input("몇명? 나는 그것이 궁굼해"))

if filter_image_path == "fail":
    sys.exit()#고칠예정(maybe)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

landmark_168 = []
x = []
y = []

landmark_9 = []
landmark_9_y = []

landmark_6 = []
landmark_6_y = []

filter_width = []
filter_height = [] 



with mp_face_mesh.FaceMesh(
        max_num_faces=people_number,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh: #1.얼굴 감지 갯수,2.랜드마크 정밀 조작,3.얼굴 감지 정확도 최소,4.얼굴 추적 최소 정확도.
    while cap.isOpened():#웹캠 열려있을 때.
        success, image = cap.read()#프레임 읽어오는 함수 success = 제대로 읽혔는지 image = 프레임별 이미지
        if not success:
            print("웹캠을 찾을 수 없습니다,큰일났습니다.")
            break

        image.flags.writeable = False #cv 성능 최적화를 위해 사용but 오류 가능성 있어서 잠시 봉인
        results = face_mesh.process(image)#얼굴 렌드마크 처리
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)#rgb값으로 변경

        if results.multi_face_landmarks:
            use_number = 0

            if frame_image_path != 0:
                image = picture.frame_image(image,frame_image_path)


            for i, face_landmarks in enumerate( results.multi_face_landmarks):     

                


                x = face_landmarks.landmark[197].x * image_width
                y = face_landmarks.landmark[197].y * image_height
                landmark_225_x = int(face_landmarks.landmark[225].x*image_width)
                landmark_446_x = int(face_landmarks.landmark[446].x*image_width)
                landmark_9_y = int(face_landmarks.landmark[9].y * image_height)
                landmark_6_y = int(face_landmarks.landmark[6].y * image_height)
                filter_width = landmark_446_x - landmark_225_x
                filter_height = int(filter_width * 0.5)

                
                #print("landmark_x",landmark_446_x,landmark_225_x)
                #print("landmark_y",landmark_6_y,landmark_9_y)
                #print("width,height",filter_width,filter_height)
                #print(f'x{x} y{y}') 

                a = landmark_446_x - landmark_225_x
                b = int(face_landmarks.landmark[446].y*image_height) - int(face_landmarks.landmark[225].y*image_height) 


                #print(f'degree예정:{a}   {b}')
                rad = math.atan2(a,b)
                deg = rad*180 //math.pi
                #print(f'deg{deg}')
                
                
                if x != None and y != None:
                    if filter_image_path != 0:
                        image = picture.take_pictures_start(filter_image_path,image,
                                                    x,y,filter_width*2,filter_height*2,use_number,(deg-82)*(-1))
                        use_number += 1

                #if image == None or image == 0:
                #    breakz
                
                #print(image.shape)
                key = cv2.waitKey(1) & 0xFF
                
                
                if key == ord('b'):
                    filter_number = int(input("필터 골라"))
                    filter_image_path = filter.checknumber(filter_number)

                elif key == ord('n'):
                    frame_number = int(input("필터 프레임 골라"))
                    frame_image_path = filter.frame_filter(frame_number)


                elif key ==ord('p'):
                    count = count + 1
                    picture.pull_image(image,count)


            cv2.imshow('image', cv2.flip(image, 1))
            if cv2.waitKey(1) & 0xFF == ord('q'):#q를 누르면 while 문 나가기
                
                break
            
cap.release()#비디오 캡쳐 창 끄기(if 문 안에 break대신 넣을 예정)
