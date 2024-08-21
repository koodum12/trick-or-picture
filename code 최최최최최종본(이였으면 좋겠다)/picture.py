import mediapipe
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils


def take_pictures_start(filter_image_path,image,
                       x,y,filter_width,filter_height,use_number,deg):

    
  x,y = int(x),int(y)
  i_h,i_w,_ = image.shape
  filter_width,filter_height = int(filter_width/2),int(filter_height/2)
  if use_number == 0:
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
  f_w,_,_ = filter_image.shape
  print(type(f_w))
  ratio = filter_width / f_w
  
  filter_height = int(filter_height / ratio)
  print(filter_width,filter_height)

  filter_image = cv2.resize(filter_image,dsize=(filter_width*2,filter_height*2))
  filter_image = imutils.rotate_bound(filter_image,0)

  filter_alpha = filter_image[:, : ,3]
  filter_mask = filter_alpha / 255
  """
  for h in range(filter_height):
    for w in range(filter_width):
      if filter_image[h,w,3] > 0:
        if h<filter_height/2 and w<filter_width/2:
          image[y-h,x-w] = image[h,x]
        elif h<filter_height/2:
          image[y+h,x-w] = image[h,x]
        elif w<filter_width/2:
          image[y-h,x+w] = image[h,x]
        else:
          image[y+h,x+w] = image[h,x]
  """
  for i in range(0,3):
    print(filter_image[:, : , i].shape,image[y-filter_height:y+filter_height, x - filter_width :x + filter_width,i].shape)

    if filter_width + x + 10 >i_w or x - filter_width - 10 < 0:
      return image
    
    if filter_height + y + 10 >i_h or y - filter_height - 10 < 0:
      return image
    
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
