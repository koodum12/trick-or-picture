import cv2
import mediapipe as mp # 구글에서 불러온 mediapipe 라이브러리 불러오기
import sys 
import filter #필터라는 라이브러리가 다른게 또 있네?
import picture
import time


image_width = 640              
image_height = 480 

#mp_drawing = mp.solutions.drawing_utils #랜드마크 표시
#mp_drawing_styles =mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) 
mp_face_mesh = mp.solutions.face_mesh

filter_number = int(input())
filter_image_path = filter.checknumber(filter_number)

if filter_image_path == "fail":
    sys.exit()#고칠예정(maybe)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_face_mesh.FaceMesh(
        max_num_faces=10,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh: #1.얼굴 감지 갯수,2.랜드마크 정밀 조작,3.얼굴 감지 정확도 최소,4.얼굴 추적 최소 정확도.
    while cap.isOpened():#웹캠 열려있을 때.
        time.sleep(1)
        success, image = cap.read()#프레임 읽어오는 함수 success = 제대로 읽혔는지 image = 프레임별 이미지
        if not success:#
            print("웹캠을 찾을 수 없습니다,큰일났습니다.")
            break

        #image.flags.writeable = False #cv 성능 최적화를 위해 사용but 오류 가능성 있어서 잠시 봉인
        results = face_mesh.process(image)#얼굴 렌드마크 처리
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#rgb값으로 변경

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmark_168 = face_landmarks.landmark[168]
                landmark_168_x = int(landmark_168.x * image_width)
                landmark_168_y = int(landmark_168.y * image_height)

                landmark_225 = face_landmarks.landmark[225]
                landmark_225_x = int(landmark_225.x*image_width)

                landmark_446 = face_landmarks.landmark[446]
                landmark_446_x = int(landmark_446.x*image_width)

                landmark_9 = face_landmarks.landmark[9]
                landmark_9_y = int(landmark_9.y * image_height)

                landmark_6 = face_landmarks.landmark[6]
                landmark_6_y = int(landmark_6.y * image_height)

                filter_width = landmark_446_x - landmark_225_x
                filter_height = landmark_6_y - landmark_9_y 
                print(filter_height,filter_width)


                #print(landmark_168_x, landmark_168_y)
                #1.이미지 파일 경로  2. 기본 이미지(동영상) 3.x좌표 4.y좌표
                save_image = picture.start_take(
                    filter_image_path,image,landmark_168_x,landmark_168_y,
                    filter_height,filter_width,
                    landmark_225_x,landmark_446_x,landmark_9_y,landmark_6_y
                    )#프레임 단위로 실시간 이미지 변수 처리.
                
            if cv2.waitKey(1) & 0xFF ==ord('p'):
                picture.picture_save(save_image)

            save_image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            cv2.imshow('MediaPipe Face Mesh(Puleugo)', cv2.flip(save_image, 1))#
            if cv2.waitKey(1) & 0xFF == ord('q'):#q를 누르면 while 문 나가기
            
                break
        
        '''
            1.영상 촬영 정지
            2.landmark표시 정지
            3.그 안에 있는 모든 것.
        '''
cap.release()#비디오 캡쳐 창 끄기(if 문 안에 break대신 넣을 예정)
