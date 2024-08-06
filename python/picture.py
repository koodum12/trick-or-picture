import cv2
import mediapipe as mp
import keyboard
from PIL import Image



def start_take(filter_image_path,mp_drawing,face_landmarks,mp_face_mesh,landmark_index,image):#filter이미지 만든 후 꼭 매게변수 추가하기
 
  filter_image = cv2.imread(filter_image_path,cv2.IMREAD_COLOR)
  filter_image = cv2.imread(filter_image_path,cv2.COLOR_BGR2RGB)
  #face_point = .landmark.landmark_index
  if filter_image is None:
          print("이미지? 그게 뭐꼬? 그런거 없으니까 돌아가라")
          return None
  
  mp_drawing_styles = mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) #랜드마크 위에 object를 어떻게 띄울지 (mediapipe 함수)
  save_image = mp_drawing.draw_landmarks(
    image=image,
    landmark_list=face_landmarks,
    connections=mp_face_mesh.FACEMESH_IRISES,
    landmark_drawing_spec=None,connection_drawing_spec=mp_drawing_styles)
  
  return save_image
    
def picture_save(save_image):
  print(1)
  return 0