import socketio
import cv2
import mediapipe as mp
import numpy as np
import math
import filter_, picture
import base64
import asyncio

sio = socketio.AsyncClient()

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1, 
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

image_height = 480
image_width = int(height * 1.77)
# FaceMesh 및 필터 적용 함수
def apply_face_mesh(image, face_mesh, filter_image_path):
    results = face_mesh.process(image)
    print(1)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            x = int(face_landmarks.landmark[1].x * image_width)
            y = int(face_landmarks.landmark[1].y * image_height)
            landmark_152_y = int(face_landmarks.landmark[152].y * image_height)
            landmark_10_y = int(face_landmarks.landmark[10].y * image_height)
            
            filter_height = abs(landmark_10_y - landmark_152_y)
            filter_width = int(filter_height * 0.5)
            b = landmark_152_y - landmark_10_y
            
            rad = math.atan2(filter_height, b)
            deg = rad * 180 / math.pi
            
            image = picture.take_pictures_start(
                filter_image_path, image, x, y, 
                filter_width * 2, filter_height * 2, 
                int(deg - 90)
            )
            cv2.imshow('image',image)
    return image

# 소켓으로 수신한 이미지를 처리하는 이벤트
@sio.on('input')
async def receive_image(data):
    global face_mesh
    # Socket으로 넘어온 데이터: 이미지(base64), filter_number, people_number
    img_data = base64.b64decode(data['image'] + '==')
    np_arr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    filter_number = data['filter_number']
    print(filter_number)
    
    # 필터 이미지 경로 설정
    filter_image_path = filter_.checknumber(filter_number)
        
    np_arr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        print("Failed to decode image")
        return  # 이미지 디코딩에 실패하면 함수 종료

    # 디코딩이 성공하면 RGB로 변환
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    image = apply_face_mesh(image, face_mesh, filter_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 필터링된 이미지를 다시 Base64로 인코딩하여 전송
    _, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    await sio.emit('output', jpg_as_text)  # 필터링된 이미지 전송

# @sio.event
# async def connect():
#     await sio.emit('re')

async def main():
    await sio.connect('http://192.168.1.26:8888')  
    await sio.emit('register', {'role': 'ai'})
    await sio.wait()

asyncio.run(main())

face_mesh.close()