import mediapipe
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import math
from skimage.transform import rotate


def take_pictures_start(filter_image_path, image,
                       x, y, filter_width, filter_height, deg):

    image = np.array(image, copy=True)
    
    x, y = int(x), int(y)
    i_h, i_w, _ = image.shape
    filter_width, filter_height = int(filter_width / 2), int(filter_height / 2)

    if x is None:
        return image

    if filter_image_path is None:
        return image

    if filter_width < 5 or filter_height < 5:
        print("filte가 안보일텐데(filter_width,filter_height) 크기가 0임")
        return image

    if image is None or image.shape[0] <= 0 or image.shape[1] <= 0:
        raise ValueError("이미지 사이즈가 왜 0? 이건 좀.")

    filter_image = cv2.imread(filter_image_path, cv2.IMREAD_UNCHANGED)
    if filter_image is None:
        print("필터 이미지를 불러올 수 없습니다.")
        return image

    filter_image = cv2.resize(filter_image, (filter_width * 2, filter_height * 2))

    # 각도를 반대로 회전하게 수정
    filter_image = imutils.rotate_bound(filter_image, (deg))  # 회전 각도 부호를 반대로 수정
    

    filter_rgb = filter_image[:, :, :3]
    filter_alpha = filter_image[:, :, 3] / 255

    # 필터 위치 계산
    h, w, _ = filter_image.shape
    top_left_x = max(0, x - w // 2)
    top_left_y = max(0, y - h // 2)
    bottom_right_x = min(i_w, x + w // 2)
    bottom_right_y = min(i_h, y + h // 2)

    # 필터 이미지의 좌표 범위 계산
    filter_top_left_x = max(0, (w // 2) - x)  
    filter_top_left_y = max(0, (h // 2) - y)
    filter_bottom_right_x = filter_top_left_x + (bottom_right_x - top_left_x)
    filter_bottom_right_y = filter_top_left_y + (bottom_right_y - top_left_y)

    # image의 크기
    image_height, image_width, image_channels = image.shape

    # filter_rgb, filter_alpha의 크기
    filter_rgb_height, filter_rgb_width, filter_rgb_channels = filter_rgb.shape
    filter_alpha_height, filter_alpha_width = filter_alpha.shape

    # 인덱스가 배열 크기를 벗어나지 않도록 확인
    if (0 <= top_left_x < bottom_right_x <= image_width and
        0 <= top_left_y < bottom_right_y <= image_height and
        0 <= filter_top_left_x < filter_bottom_right_x <= filter_rgb_width and
        0 <= filter_top_left_y < filter_bottom_right_y <= filter_rgb_height):
        
        for i in range(3):
            image[top_left_y:bottom_right_y, top_left_x:bottom_right_x, i] = (
                filter_rgb[filter_top_left_y:filter_bottom_right_y, filter_top_left_x:filter_bottom_right_x, i] *
                filter_alpha[filter_top_left_y:filter_bottom_right_y, filter_top_left_x:filter_bottom_right_x] +
                image[top_left_y:bottom_right_y, top_left_x:bottom_right_x, i] *
                (1 - filter_alpha[filter_top_left_y:filter_bottom_right_y, filter_top_left_x:filter_bottom_right_x])
            )
    else:
        print("인덱스 범위가 이미지 크기를 벗어났습니다.")

    return image



