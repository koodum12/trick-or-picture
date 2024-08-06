import cv2
from PIL import Image
import filter
import mediapipe

def checknumber(filter_number):
  match filter_number:
    case 0:
      return None
    case 1:   
      filter_image = fr'C:\Users\user\Desktop\Obsidian\trick-or-picture\img\{filter_number}.png'
      return filter_image
    
  print("이 오류 뭐임? 어케 냄?")
  return "fail"

      
#1.도트 썬글라스
#2.부터 정해야 하는데.... 이미지가 없다!