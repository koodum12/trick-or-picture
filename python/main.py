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
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("웹캠을 찾을 수 없습니다.")

            break

        image.flags.writeable = True
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                save_image = picture.start_take(mp_drawing,image,face_landmarks,mp_face_mesh)
                
            keyboard.add_hotkey('p',picture.picture_save(save_image))#사용자 지정 함수 넣을 예정
                            
        image_bgr = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        cv2.imshow('MediaPipe Face Mesh(Puleugo)', cv2.flip(image_bgr, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
