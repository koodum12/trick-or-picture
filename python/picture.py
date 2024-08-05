import cv2
import mediapipe as mp
import keyboard

def __init__(self):
    pass

def start_take(mp_drawing,image,face_landmarks,mp_face_mesh):
  
  mp_drawing_styles =mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) #랜드마크 위에 object를 어떻게 띄울지 (mediapipe 함수)
  save_image = mp_drawing.draw_landmarks(
    image=image,
    landmark_list=face_landmarks,
    connections=mp_face_mesh.FACEMESH_IRISES,
    landmark_drawing_spec=None,connection_drawing_spec=mp_drawing_styles)
  
  return save_image
    
def picture_save(save_image):
  #cv2.imshow('o',save_image)
  print(1)
  return 