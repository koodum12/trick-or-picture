import mediapipe
import cv2
import numpy as np


def take_pictures_start(filter_image_path,image,
                       x,y,filter_width,filter_height):
    
  x,y = int(x),int(y)
  i_h,i_w,_ = image.shape
  filter_width,filter_height = int(filter_width/2),int(filter_height/2)
  image = cv2.cvtColor(image,cv2.COLOR_BGR2RGBA)

  if filter_image_path is None:
    print("이미지? 그게 뭐꼬? 그런거 없으니까 돌아가라")
    return None
  

  if filter_width == 0 or filter_height == 0:
    print("filte가 안보일텐데(filter_width,filter_height) 크기가 0임")
  else:
    print("width,height",filter_width,filter_height)
    

  if image is None or image.shape[0] <= 0 or image.shape[1] <= 0:
    raise ValueError("이미지 사이즈가 왜 0? 이건 좀.")
  

  
  

  filter_image = cv2.imread(filter_image_path, cv2.IMREAD_UNCHANGED)
  filter_image = cv2.resize(filter_image,dsize=(filter_width*2,filter_height*2))
  filter_alpha = filter_image[:, : ,3]
  filter_mask = filter_alpha / 255
  for i in range(0,3):
    print(filter_image[:, : , i].shape,image[y-filter_height:y+filter_height, x - filter_width :x + filter_width,i].shape)
    image[y-filter_height : y+filter_height ,x-filter_width:x + filter_width,i] = (
      (filter_image[:, : , i] * filter_mask) + 
      (image[y-filter_height:y+filter_height, x - filter_width :x + filter_width,i] * ( 1 - filter_mask ))
      )

    

  return image



def pull_image(save_image,count):

  if count < 4:
    save_image = cv2.flip(save_image, 1)
    cv2.imwrite(f"{count}_filter_image.jpg", save_image)
    print("이미지 저장 완료")

  elif count == 4:
    save_image = cv2.flip(save_image, 1)
    cv2.imwrite(f"{count}_filter_image.jpg", save_image)
    print("이미지 촬영 종료")

  else:
     raise ValueError(fr'"인생 4컷 임마 인생 4컷 인생 {count}컷이 아니라"')
  return 0
