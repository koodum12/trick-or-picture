import cv2
import filter
import asyncio




def face_filter_input(filter_number):
    input_number = int(input("필터 다시 정해봐"))
    if -1 <input_number < 3:
        return input_number
    else:
         return filter_number
        
def frame_filter_input(frame_number):
        input_number = int(input('프레임 이미지 다시 정해봐'))
        if -1 <input_number < 3:
            return input_number
        else:
             return frame_number
        

