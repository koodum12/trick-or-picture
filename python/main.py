import cv2
import mediapipe as mp # 구글에서 불러온 mediapipe 라이브러리 불러오기 
import keyboard
import picture

mp_drawing = mp.solutions.drawing_utils #랜드마크 표시
mp_drawing_styles =mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) #
mp_face_mesh = mp.solutions.face_mesh

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

        image.flags.writeable = False
        results = face_mesh.process(image)#얼굴 렌드마크 처리

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#rgb값으로 변경
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                save_image = picture.start_take(mp_drawing,image,face_landmarks,mp_face_mesh)#프레임 단위로 실시간 이미지 변수 처리.
            
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
