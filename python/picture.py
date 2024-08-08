import cv2
import mediapipe as mp
import keyboard
from PIL import Image



import numpy as np

def start_take(filter_image_path, image, landmark_168_x, landmark_168_y):
    # 필터 이미지 로드 (알파 채널 포함)
    filter_image = cv2.imread(filter_image_path, cv2.IMREAD_UNCHANGED)
    
    if filter_image is None:
        raise ValueError("Filter image not found or unable to load.")
    
    # 필터 이미지에 알파 채널이 없는 경우 처리
    if filter_image.shape[2] == 3:
        raise ValueError("Filter image does not have an alpha channel.")

    # 필터 이미지 크기 조정
    filter_image = cv2.resize(filter_image, (50, 100))

    # 알파 채널 분리
    filter_alpha = filter_image[:, :, 3] / 255.0
    filter_rgb = filter_image[:, :, :3]

    image_alpha = 1.0 - filter_alpha

    # 적용 영역 계산
    x1, y1 = landmark_168_x, landmark_168_y
    x2, y2 = x1 + filter_image.shape[1], y1 + filter_image.shape[0]

    # 이미지 경계를 넘어가지 않도록 조정
    if x2 > image.shape[1]:
        x2 = image.shape[1]
    if y2 > image.shape[0]:
        y2 = image.shape[0]
    
    if x1 < 0: x1 = 0
    if y1 < 0: y1 = 0

    # 조정된 크기에 맞게 필터 이미지 조정
    filter_rgb = filter_rgb[:y2-y1, :x2-x1]
    filter_alpha = filter_alpha[:y2-y1, :x2-x1]
    image_alpha = image_alpha[:y2-y1, :x2-x1]

    # 원본 이미지에서 ROI 선택
    roi = image[y1:y2, x1:x2]

    # 필터 적용
    for c in range(3):  # 3 채널 (RGB)
        roi[:, :, c] = (filter_alpha * filter_rgb[:, :, c] + image_alpha * roi[:, :, c])

    image[y1:y2, x1:x2] = roi

    return image

    
def picture_save(save_image):
  print(1)
  return 0