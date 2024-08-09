import cv2
import mediapipe as mp
import imutils
from math import hypot



def start_take(filter_image_path,image,x,y,
               landmark_225_x,landmark_446_x,landmark_9_y,landmark_6_y):#filter이미지 만든 후 꼭 매게변수 추가하기
  #face_point = .landmark.landmark_index
  if filter_image_path is None:
          print("이미지? 그게 뭐꼬? 그런거 없으니까 돌아가라")
          return None
  image = imutils.resize(image, width=750,height = 500)

  filter_image = cv2.imread(filter_image_path,cv2.IMREAD_UNCHANGED)

  filter_image = cv2.resize(filter_image,(filter_height,filter_width)) #filter이미지 크기 조절(조정 예정)


  filter_width = int(hypot(landmark_446_x-landmark_225_x, landmark_9_y-landmark_6_y*1.2))
  filter_height = int(filter_width*0.77)

  if filter_width != 0:
      filter_image = cv2.resize(filter_image(filter_width,filter_height))

  top_left = (int(x-filter_width/2),int(y-filter_height/2))
  bottom_right = (int(x+filter_width/2),int(y+filter_height/2))
  #------------------------------------------------------------------------- 여기서부터 고칠거임

  '''
  #[행:열:]
  filter_alpha = filter_image[:,3] /255.0

  image_alpha = 1.0 - filter_alpha

  image[x:y,50:100] = filter_alpha * filter_image[:,3] + image_alpha * filter_image[:,3]
  return image
  '''

  '''mp_drawing_styles = mp_drawing.DrawingSpec(color=(0,0,0),thickness = 10 ) #랜드마크 위에 object를 어떻게 띄울지 (mediapipe 함수)
  save_image = mp_drawing.draw_landmarks(
    image=image,
    landmark_list=face_landmarks,
    connections=mp_face_mesh.FACEMESH_IRISES,
    landmark_drawing_spec=None,connection_drawing_spec=mp_drawing_styles)
  '''
  #return save_image
    
def picture_save(save_image):
  print(1)
  return 0