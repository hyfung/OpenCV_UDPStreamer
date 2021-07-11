import cv2, numpy as np
import os, sys
import socket
import threading, queue
import time
import signal

q = queue.Queue()
run = True

def sigint_handler(signum, frame):
    # This function is called when Ctrl-C or SIGINT is received
    # Exit gracefully
    global run
    run = False

def captureThread():
    cap = cv2.VideoCapture(0)
    
    while run:
        ret, img = cap.read()
        img = cv2.resize(img, (320,240))
        ret, img_encode = cv2.imencode('.jpg', img)
        q.put(img_encode.tobytes())
        cv2.imshow("Transmitting Feed", img)
        cv2.waitKey(100)

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    tCapture = threading.Thread(target=captureThread)
    tCapture.start()

    count = 0
    while run:
        client.sendto(q.get(), ("127.0.0.1", 9999))
        time.sleep(0.1)
        print(f'[Send] {count}')
        count += 1

if __name__ == '__main__':
    main()
