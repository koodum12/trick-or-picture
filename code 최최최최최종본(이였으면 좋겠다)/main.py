import socketio
import cv2
import mediapipe as mp
import numpy as np
import math
import filter_, picture
import base64
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 소켓 클라이언트 초기화 및 재연결 설정
sio = socketio.AsyncClient(
    reconnection=True,
    reconnection_attempts=10,
    reconnection_delay=1,
    reconnection_delay_max=5
)

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, 
    refine_landmarks=True,
    min_detection_confidence=0.2,
    min_tracking_confidence=0.2
)

executor = ThreadPoolExecutor(max_workers=4)  # 이미지 처리를 위한 스레드 풀

def calculate_face_angle(face_landmarks, image_width, image_height):
    try:
        left_eye = [
            (face_landmarks.landmark[33].x + face_landmarks.landmark[133].x) / 2,
            (face_landmarks.landmark[33].y + face_landmarks.landmark[133].y) / 2
        ]
        right_eye = [
            (face_landmarks.landmark[362].x + face_landmarks.landmark   [263].x) / 2,
            (face_landmarks.landmark[362].y + face_landmarks.landmark[263].y) / 2
        ]
        
        nose = [face_landmarks.landmark[4].x, face_landmarks.landmark[4].y]
        mouth = [
            (face_landmarks.landmark[61].x + face_landmarks.landmark[291].x) / 2,
            (face_landmarks.landmark[61].y + face_landmarks.landmark[291].y) / 2
        ]
        
        dx = (right_eye[0] - left_eye[0]) * image_width
        dy = (right_eye[1] - left_eye[1]) * image_height
        eye_angle = math.degrees(math.atan2(dy, dx))
        final_angle = max(-45, min(45, eye_angle))
        
        return final_angle
    except Exception as e:
        logger.error(f"Error calculating face angle: {e}")
        return 0  # 기본 각도로 설정

def apply_face_mesh_sync(image, face_mesh, filter_image_path):
    try:
        image_height, image_width, _ = image.shape
        results = face_mesh.process(image)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                angle = calculate_face_angle(face_landmarks, image_width, image_height)
                
                x = int(face_landmarks.landmark[1].x * image_width)
                y = int(face_landmarks.landmark[1].y * image_height)
                
                x1 = face_landmarks.landmark[152].x * image_width
                y1 = face_landmarks.landmark[152].y * image_height
                x2 = face_landmarks.landmark[10].x * image_width
                y2 = face_landmarks.landmark[10].y * image_height
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                filter_height = int(distance)
                filter_width = int(filter_height * 0.5)
                
                image = picture.take_pictures_start(
                    filter_image_path, image, x, y,
                    filter_width * 2, filter_height * 2,
                    int(angle)
                )
        return image
    except Exception as e:
        logger.error(f"Error applying face mesh: {e}")
        return image  # 처리에 실패해도 원본 이미지 반환

async def apply_face_mesh_async(image, face_mesh, filter_image_path):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        executor, 
        apply_face_mesh_sync, 
        image, 
        face_mesh, 
        filter_image_path
    )

# 소켓 이벤트 핸들러
@sio.event
async def connect():
    logger.info("Connected to the server.")
    await sio.emit('register', {'role': 'ai'})

@sio.event
async def disconnect():
    logger.warning("Disconnected from the server.")

@sio.on('input')
async def receive_image(data):
    try:
        img_data = base64.b64decode(data['image'] + '==')
        np_arr = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        filter_number = data.get('filter_number', 0)
        logger.info(f"Received filter number: {filter_number}")

        filter_image_path = filter_.checknumber(filter_number)

        if image is None:
            logger.error("Failed to decode image")
            return

        # BGR에서 RGB로 변환
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = True

        # 비동기로 이미지 처리
        processed_image = await apply_face_mesh_async(image, face_mesh, filter_image_path)

        # RGB에서 BGR로 변환
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR)

        # 필터링된 이미지를 Base64로 인코딩
        _, buffer = cv2.imencode('.jpg', processed_image)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        await sio.emit('output', jpg_as_text)
        logger.info("Processed image sent successfully.")

    except Exception as e:
        logger.error(f"Error during image processing: {e}")

async def main():
    try:
        await sio.connect('http://121.159.74.206:8888', transports=['websocket'])
        await sio.wait()
    except Exception as e:
        logger.error(f"Socket connection error: {e}")
    finally:
        face_mesh.close()
        executor.shutdown(wait=True)
        logger.info("Resources have been cleaned up.")

# 서버와 연결 및 대기
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")