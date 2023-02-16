# import library yang dibutuhkan
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import threading
import time
import pyautogui
import mouse

detector = HandDetector(detectionCon=0.9, maxHands=1) # define HandDetector yang diambil dari lib cvzone
cap = cv2.VideoCapture(0) # menentukan hardware kamera
cam_w, cam_h = 640, 480 # mengatur resolusi gambar
cap.set(3, cam_w)
cap.set(4, cam_h)

frameR = 100 
l_delay = 0

def l_clk_delay(): # function untuk memulai thread ketika gesture tombol kiri mouse
    global l_delay
    global l_clk_thread
    time.sleep(1)
    l_delay = 0
    l_clk_thread = threading.Thread(target=l_clk_delay)

l_clk_thread = threading.Thread(target=l_clk_delay)

while True: # memulai perulangan 
    success, img = cap.read() # membuka mengambil gambar
    img = cv2.flip(img, 1) 
    hands, img = detector.findHands(img, flipType=False) #melakukan deteksi tangan berdasarkan gambar yang telah diambil

    if hands: # jika tangan ditemukan
        lmlist = hands[0]["lmList"] # menentukan ruas jari jari tangan
        ind_x, ind_y = lmlist[8][0], lmlist[8][1] # index ujung jari
        thumb_x, thumb_y = lmlist[4][0], lmlist[4][1] # ibu jari
        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2) # menggambar ujung jari telunjuk dengan warna kuning
        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2) # menggambar ujung ibu jari dengan warna kuning
        fingers = detector.fingersUp(hands[0]) # mengambil data gesture tangan
        print(fingers) # log data tangan

        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0: # menentukan gesture untuk memindahkan cursor
            conv_x = int(np.interp(ind_x, (frameR, cam_w - frameR), (0, 1536))) # mengambil data kordinat x
            conv_y = int(np.interp(ind_y, (frameR, cam_h - frameR), (0, 864))) # mengambil data kordinat y
            mouse.move(conv_x, conv_y) # memindahkan cursor

        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 1: # menentukan gesture untuk melakukan left click mouse
            if abs(ind_x-thumb_x) < 25:
                if l_delay == 0:
                    print("mouse kiri terclick")
                    pyautogui.click(button="left")  # menekan tombol mouse kiri
                    l_delay = 1
                    l_clk_thread.start()

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0: # menentukan gesture untuk melakukan right click mouse
            if l_delay == 0:
                print("mouse kanan terclick")
                pyautogui.click(button="right")  # menekan tombol mouse kanan

    cv2.imshow("Ini Kamera", img)
    cv2.waitKey(1)