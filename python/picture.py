import cv2
import mediapipe as mp
import imutils
from math import hypot



def start_take(filter_image_path,image,x,y,
               filter_height,filter_width,
               landmark_225_x,landmark_446_x,landmark_9_y,landmark_6_y):#filter이미지 만든 후 꼭 매게변수 추가하기
  #face_point = .landmark.landmark_index
  if filter_image_path is None:
          print("이미지? 그게 뭐꼬? 그런거 없으니까 돌아가라")
          return None
  if image is None or image.shape[0] <= 0 or image.shape[1] <= 0:
    raise ValueError("이미지 사이즈가 왜 0? 이건 좀.")
  
  if filter_height <= 0 or filter_width <= 0:
      print("크기가 왜 0?")
      filter_width = 1
      filter_height = 1
      return 0
  image = imutils.resize(image, filter_width,filter_height)

  filter_image = cv2.imread(filter_image_path,cv2.IMREAD_UNCHANGED)

  filter_image = cv2.resize(filter_image,(filter_height,filter_width)) #filter이미지 크기 조절(조정 예정)


  filter_width = int(hypot(landmark_446_x-landmark_225_x, landmark_9_y-landmark_6_y*1.2))
  filter_height = int(filter_width*0.77)

  if filter_width != 0:
      filter_image = cv2.resize(filter_image,(filter_width,filter_height))

  top_left = (int(x-filter_width/2),int(y-filter_height/2))
  bottom_right = (int(x+filter_width/2),int(y+filter_height/2))
  #------------------------------------------------------------------------- 여기서부터 고칠거임

  filter_area = image[
    top_left[1]: top_left[1]+filter_height,
    top_left[0]: top_left[0]+filter_width
    ]
  
  # nose mask 생성
  filter_mask = cv2.cvtColor(filter_image, cv2.COLOR_BGR2GRAY)
  _,filter_mask = cv2.threshold(filter_mask, 25, 255, cv2.THRESH_BINARY_INV)

  filter_mask = cv2.resize(filter_mask,(filter_width,filter_height))
  no_filter = cv2.multiply(filter_area, filter_mask / 255.0)
  
  #filter_area = cv2.bitwise_and(filter_area, filter_area, mask=filter_mask)

  # no_nose에 pig nose 중첩
  final_filter = cv2.add(no_filter, filter_image)
  # pig nose filter를 영상에 적용
  image[
    top_left[1]: top_left[1]+filter_height,
    top_left[0]: top_left[0]+filter_width
    ] = final_filter
  return image
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