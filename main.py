import cv2
import pickle
import cvzone
import numpy as np

#Video feed
cap = cv2.VideoCapture('CarParkSource/carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48

#func: 檢查停車格是否為空位
def checkParkingSpace(imgPro):
    spaceCounter = 0 # 計算停車格數

    for pos in posList:
        pos_x, pos_y = pos
        #切割出每一格停車格畫面
        imgCrop = imgPro[pos_y:pos_y + height, pos_x:pos_x + width] 
        # cv2.imshow(str(x * y), imgCrop) 
        count = cv2.countNonZero(imgCrop)

        #依像素格判斷是否為空
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) #框出停車格
        cvzone.putTextRect(img, str(count), (pos_x, pos_y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)  #標出像素個數

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0)) #標出停車格數 
   
#Video Run   
while True:
    #確認影片是否結束，是則重播
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read() #讀取下一幀
    #圖片處理
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #轉灰階
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1) #高斯模糊降噪
    #分離出目標區域與背景區域
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16) #高斯加權均值法自適應二值化
    imgMedian = cv2.medianBlur(imgThreshold, 5) #中值模糊再次降噪
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) #加粗圖片線條

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    if cv2.waitKey(5) == ord('q'):
        break