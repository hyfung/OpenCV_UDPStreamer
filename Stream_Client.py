import cv2, numpy as np
import os, sys
import socket
import threading
import time

def main():
    cap = cv2.VideoCapture(0)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    count = 0
    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (320,240))
        ret, img_encode = cv2.imencode('.jpg', img)
        client.sendto(img_encode.tobytes(), ("127.0.0.1", 9999))
        time.sleep(0.1)
        print(count)
        count += 1

if __name__ == '__main__':
    main()
