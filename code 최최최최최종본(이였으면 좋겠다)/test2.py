import cv2
import mediapipe

oepn = r'C:\Users\user\Desktop\Obsidian\trick-or-picture\img\1.png'
open = cv2.imread(oepn,cv2.COLOR_BGR2RGBA)
print(open.shape)
while 1:
  cv2.imshow("rk",open)