import mediapipe
import cv2

def take_pictures_start(filter_image_path,image,
                       filter_width,filter_height,x,y,):
  if filter_image_path is None:
    print("이미지? 그게 뭐꼬? 그런거 없으니까 돌아가라")
    return None
  
  if image is None or image.shape[0] <= 0 or image.shape[1] <= 0:
    raise ValueError("이미지 사이즈가 왜 0? 이건 좀.")
  
  filter_image = cv2.imread(filter_image_path, cv2.IMREAD_COLOR)
  filter_height,filter_width = int(filter_height),int(filter_width)
  #filter_image = cv2.resize(filter_image,(filter_height,filter_width))
  cv2.imshow('제목:돈까스 맛난다',image)

  i_h,i_w,_ = image.shape
  
  if x + filter_width > i_w or y + filter_height > i_h:
    raise ValueError("조성현 바보(20 line) (필터 이미지가 배경 이미지를 벗어났습니다)")
  


  top_left = (int(x-filter_width/2),int(y-filter_height/2))
  bottom_right = (int(x+filter_width/2),int(y+filter_height/2))

  filter_area = image[
      top_left[1]: top_left[1]+filter_height,
      top_left[0]: top_left[0]+filter_width
  ]
  #cv2.imshow("sdfasdf",filter_area)

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
