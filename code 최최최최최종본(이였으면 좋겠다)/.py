import cv2
import mediapipe as mp

# MediaPipe 초기화
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# 웹캠 비디오 캡처
cap = cv2.VideoCapture(0)

# Face Mesh 모델 초기화
with mp_face_mesh.FaceMesh(
    max_num_faces=3,  # 최대 3명의 얼굴 감지
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라에서 영상을 가져올 수 없습니다.")
            break

        # 성능을 높이기 위해 이미지를 RGB로 변환
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 얼굴 메쉬 감지 수행
        results = face_mesh.process(image)

        # 감지된 얼굴이 있는 경우
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for i, face_landmarks in enumerate(results.multi_face_landmarks):
                # 225번째 랜드마크의 좌표 추출
                x = face_landmarks.landmark[225].x
                y = face_landmarks.landmark[225].y
                z = face_landmarks.landmark[225].z

                # 이미지 상의 좌표로 변환
                ih, iw, _ = image.shape
                x_px, y_px = int(x * iw), int(y * ih)

                # 좌표 출력
                print(f"사람 {i+1} - 225번째 랜드마크 좌표: x={x_px}, y={y_px}, z={z}")

                # 랜드마크 위치에 원 그리기
                cv2.circle(image, (x_px, y_px), 5, (0, 255, 0), -1)

        # 결과를 화면에 표시
        cv2.imshow('MediaPipe Face Mesh', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
