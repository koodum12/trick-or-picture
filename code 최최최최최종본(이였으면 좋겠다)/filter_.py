import cv2
import mediapipe
import os

def checknumber(filter_number):
    # 필터 번호가 0일 경우, None 반환
    if filter_number == 0:
        return None
    
    # 이미지 경로 생성
    filter_image_path = fr'C:\Users\user\Desktop\Obsidian\trick-or-picture\img\{filter_number}.png'
    print(filter_image_path)

    # 파일 존재 여부 확인
    if os.path.isfile(filter_image_path):
        return filter_image_path
    else:
        print(f"파일이 존재하지 않습니다: {filter_image_path}")
        return None


def frame_filter(frame_number):
    # 유효하지 않은 프레임 번호 처리
    if frame_number == 0 or frame_number >= 3:
        return None  # 해당하는 경로가 없을 경우 None 반환
    
    # 프레임 이미지 경로 생성
    frame_image_path = fr'C:\Users\user\Desktop\Obsidian\trick-or-picture\frame_image\{frame_number}.png'
    return frame_image_path
