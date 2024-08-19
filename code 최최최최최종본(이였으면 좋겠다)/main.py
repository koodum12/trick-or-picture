import cv2
import mediapipe as mp # 구글에서 불러온 mediapipe 라이브러리 불러오기
import sys 
import filter #필터라는 라이브러리가 다른게 또 있네?
import picture
import numpy as np

image_width = 640              
image_height = 480 
count = int(0)
#mp_drawing = mp.solutions.drawing_utils #랜드마크 표시
#mp_drawing_styles =mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) 
mp_face_mesh = mp.solutions.face_mesh

filter_number = int(input())
filter_image_path = filter.checknumber(filter_number)

people_number = int(input())
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
        if not success:#
            print("웹캠을 찾을 수 없습니다,큰일났습니다.")
            break

        image.flags.writeable = False #cv 성능 최적화를 위해 사용but 오류 가능성 있어서 잠시 봉인
        results = face_mesh.process(image)#얼굴 렌드마크 처리
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#rgb값으로 변경

        if results.multi_face_landmarks:
            for i, face_landmarks in enumerate(results.multi_face_landmarks):                
                x = face_landmarks.landmark[103].x * image_width
                y = face_landmarks.landmark[103].y * image_height
                landmark_225_x = int(face_landmarks.landmark[225].x*image_width)
                landmark_446_x = int(face_landmarks.landmark[446].x*image_width)
                landmark_9_y = int(face_landmarks.landmark[9].y * image_height)
                landmark_6_y = int(face_landmarks.landmark[6].y * image_height)
                filter_width = landmark_446_x - landmark_225_x
                print("landmark_x",landmark_446_x,landmark_225_x)
                print("landmark_y",landmark_6_y,landmark_9_y)
                print("width,height",filter_width,filter_height)
                filter_height = (landmark_6_y - landmark_9_y)

                print(f'x{x} y{y}')
                image = picture.take_pictures_start(filter_image_path,image,
                                                    x,y,filter_width*2,filter_height*2)


            #if image == None or image == 0:
            #    breakz
            
            #print(image.shape)

            if cv2.waitKey(1) & 0xFF ==ord('p'):
                count = count + 1
                picture.pull_image(image,count)

            cv2.imshow('image', cv2.flip(image, 1))
            if cv2.waitKey(1) & 0xFF == ord('q'):#q를 누르면 while 문 나가기
            
                break
        
        '''
            1.영상 촬영 정지
            2.landmark표시 정지
            3.그 안에 있는 모든 것.
        '''
cap.release()#비디오 캡쳐 창 끄기(if 문 안에 break대신 넣을 예정)
