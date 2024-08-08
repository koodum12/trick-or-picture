import cv2
from PIL import Image
import filter
import mediapipe
import os
def checknumber(filter_number):
  match filter_number:
    case 0:
      return None
  filter_image_path = fr'C:\Users\user\Desktop\Obsidian\trick-or-picture\img\{filter_number}.png'
  
  if os.path.isfile(filter_image_path):
      return filter_image_path
  else:
      print(f"파일이 존재하지 않습니다: {filter_image_path}")
      return None

  

      
#1.도트 썬글라스
#2.부터 정해야 하는데.... 이미지가 없다!