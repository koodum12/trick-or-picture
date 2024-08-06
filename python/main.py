import cv2
import mediapipe as mp # 구글에서 불러온 mediapipe 라이브러리 불러오기
import sys 
import filter #필터라는 라이브러리가 다른게 또 있네?
import keyboard
import picture

mp_drawing = mp.solutions.drawing_utils #랜드마크 표시
mp_drawing_styles =mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) 
mp_face_mesh = mp.solutions.face_mesh

filter_number = int(input())
filter_image_path = filter.checknumber(filter_number)

if filter_image_path == "fail":
    sys.exit()#고칠예정(maybe)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh: #1.얼굴 감지 갯수,2.랜드마크 정밀 조작,3.얼굴 감지 정확도 최소,4.얼굴 추적 최소 정확도.
    while cap.isOpened():#웹캠 열려있을 때.
        success, image = cap.read()#프레임 읽어오는 함수 success = 제대로 읽혔는지 image = 프레임별 이미지
        if not success:#
            print("웹캠을 찾을 수 없습니다,큰일났습니다.")
            break

        #image.flags.writeable = False #cv 성능 최적화를 위해 사용but 오류 가능성 있어서 잠시 봉인
        results = face_mesh.process(image)#얼굴 렌드마크 처리
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#rgb값으로 변경

        landmark_index = 33 #고칠거임
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmark_168 = face_landmarks.landmark[168] #168 = 얼굴 정 중앙()
                landmark_168_x = landmark_168.x
                landmark_168_y = landmark_168.y
                #1.이미지 파일 경로 2.랜드마크 시각표현 사용 3.랜드마크 좌표 반환 4.얼굴 랜드마크와 연결정보 처리 5.사용할 landmark index 6.기본 이미지(동영상)
                save_image = picture.start_take(filter_image_path,mp_drawing,face_landmarks,mp_face_mesh,landmark_index,image)#프레임 단위로 실시간 이미지 변수 처리.
            
            if cv2.waitKey(1) & 0xFF ==ord('p'):
                picture.picture_save(save_image)
        
        image_bgr = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('MediaPipe Face Mesh(Puleugo)', cv2.flip(image_bgr, 1))#
        if cv2.waitKey(1) & 0xFF == ord('q'):#q를 누르면 while 문 나가기 
            break
        '''
            1.영상 촬영 정지
            2.landmark표시 정지
            3.그 안에 있는 모든 것.
        '''
cap.release()#비디오 캡쳐 창 끄기(if 문 안에 break대신 넣을 예정)
