import cv2
import filter
import mediapipe
import os
def checknumber(filter_number):
    if filter_number == int(0):
        return 0
    
    filter_image_path = fr'C:\Users\user\Desktop\Obsidian\trick-or-picture\img\{filter_number}.png'
    print(filter_image_path)

    if os.path.isfile(filter_image_path):
        return filter_image_path
  
    else:
        print(f"파일이 존재하지 않습니다: {filter_image_path}")
        return None


#1.도트 썬글라스
#2.부터 정해야 하는데.... 이미지가 없다!


def frame_filter(frame_number):

    if frame_number == 0:
        return 0
    if frame_number >= 3:
        return None
    frame_image_path = fr'C:\Users\user\Desktop\Obsidian\trick-or-picture\frame_image\{frame_number}.png'

    return frame_image_path

      
#1.크리스마스 느낌 프레임
#2.필름 프레임
#3.부터 정해야 하는데.... 이미지가 없다!