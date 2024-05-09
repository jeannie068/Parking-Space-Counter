import cv2
import pickle # 檔案

width, height = 107, 48
# 達到保存 posList 資料的功用
try: # 查看是否已有'CarParkingPos'的檔案存在
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# 建立滑鼠點擊功能的函式
def mouse_click(events, x, y, flags, params):
    # 如果點擊滑鼠左鍵
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y)) #將左上角座標記錄下來
    # 如果點擊滑鼠右鍵
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            pos_x, pos_y = pos
            # 偵測是否有方框可以刪除
            if pos_x < x < pos_x+width and pos_y < y < pos_y + height:
                posList.pop(i) # 將posList中不要的左上角座標刪掉，即把畫錯的正方格從畫面中刪掉
    # 創建檔案紀錄已儲存的左上角座標
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)  # 使用 dump 把 posList 倒進去 f 裡面

# while 迴圈使圖片可更新狀態
while True:
	img = cv2.imread('CarParkSource/carParkImg.png')
	for pos in posList:
		cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255, 0, 255), 2) #粗度2 紫色的方框
	cv2.imshow('image', img)
	cv2.setMouseCallback('image', mouse_click) #偵測滑鼠事件，並使用前面定義的函式
	if cv2.waitKey(1) == ord('q'): #中斷程式
          break