import mediapipe
import cv2
import numpy as np


def take_pictures_start(filter_image_path,image,
                       x,y,filter_width,filter_height):
  if filter_image_path is None:
    print("이미지? 그게 뭐꼬? 그런거 없으니까 돌아가라")
    return None
  if filter_width == 0 or filter_height == 0:
    print("10번 오류")
  else:
    print("width,height",filter_width,filter_height)
    
  if image is None or image.shape[0] <= 0 or image.shape[1] <= 0:
    raise ValueError("이미지 사이즈가 왜 0? 이건 좀.")
  
  filter_image = cv2.imread(filter_image_path, cv2.IMREAD_UNCHANGED)
  cv2.imshow("filter_image",filter_image)
  print(f'filter_image.shape:{filter_image.shape}')
  if filter_width != 0:
      filter_image = cv2.resize(filter_image,(filter_width ,filter_height))
  else:
    print("size change error (filter_image)")

  image = cv2.cvtColor(image,cv2.COLOR_BGR2RGBA)

  filter_height,filter_width = int(filter_height),int(filter_width)
  #filter_image = cv2.resize(filter_image,(filter_height,filter_width))
  cv2.imshow('제목:돈까스 맛난다',image)

  i_h,i_w,_ = image.shape
  
  if x + filter_width > i_w or y + filter_height > i_h:
      raise ValueError("조성현 바보(20 line) (필터 이미지가 배경 이미지를 벗어났습니다)")
  
  top_left = (int(x-filter_width/2),int(y-filter_height/2))

  print("1: ",i_h)
  print("2: ",i_w)
  print(image)
  x = int(x) 
  y = int(y)
  filter_area = image[
      y: y+filter_height,
      x: x+filter_width
  ] 
  if filter_area.shape[0] == 0 or filter_area.shape[1] == 0:
    print(f"filter_area의 크기가 0이거나 유효하지 않습니다. top_left 좌표: {top_left}, 필터 너비: {filter_width}, 필터 높이: {filter_height}")
  cv2.imshow("바보멍충이",filter_area)
  filter_mask = filter_image
  _,filter_mask = cv2.threshold(filter_mask, 25, 255, cv2.THRESH_BINARY_INV)
  filter_area = filter_area.astype('uint8')
  filter_mask = filter_mask.astype('uint8')


  try:
    filter_mask = cv2.resize(filter_mask,(filter_width,filter_height))
    filter_mask = cv2.cvtColor(filter_mask, cv2.COLOR_BGR2RGB)

    print(filter_mask.shape)
  except:
     print("63")
     return 0
  

  try:
    filter_area = cv2.resize(filter_area,(filter_width,filter_height))
    filter_area = cv2.cvtColor(filter_area, cv2.COLOR_BGR2RGB)

    print(filter_mask.shape)
  except:
     print("67")
     return 0
  
  print(filter_area.dtype)  # 확인
  print(filter_mask.dtype)  # 확인

  scale = 1.0
  offset = 128

  filter_mask = (scale * filter_mask + offset).astype(np.uint8)
  filter_area = (scale * filter_mask + offset).astype(np.uint8)

  print("Filter area shape:", filter_area.shape, "dtype:", filter_area.dtype)
  print("Filter mask shape:", filter_mask.shape, "dtype:", filter_mask.dtype)
  filter_mask_gray = cv2.cvtColor(filter_mask, cv2.COLOR_RGB2GRAY)

  # 마스크가 유효한 범위(0-255)의 값을 가지도록 확실히 합니다.
  filter_mask_gray = cv2.normalize(filter_mask_gray, None, 0, 255, cv2.NORM_MINMAX)
  filter_mask_gray = np.uint8(filter_mask_gray)
    #try:
  no_filter = cv2.bitwise_and(filter_area, filter_area, mask=filter_mask_gray)
  #except:
  #  
  #  return None
  print(f'no_filter{no_filter.shape} filter_mask{filter_image.shape}')
  final_filter = cv2.add(no_filter, filter_image)
  final_filter = cv2.cvtColor(final_filter,cv2.COLOR_BGR2RGBA)
  #final_filter = cv2.cvtColor(final_filter,cv2.IMREAD_UNCHANGED)

  print(f'final_filter:{final_filter.shape}')
  print(y,x)
  image[
      y: y+filter_height,
      x: x+filter_width
    ] = final_filter

  print(filter_area.shape)

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
