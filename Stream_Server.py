import cv2, numpy as np
import os, sys
import socket
import threading, queue
import time

q = queue.Queue()

def displayThread():
    while True:
        data = q.get()
        tmp = np.asarray(bytearray(data), dtype='uint8')
        img = cv2.imdecode(tmp, cv2.IMREAD_COLOR)
        cv2.imshow("Window", img)
        cv2.waitKey(100)

def main():
    img = None
    bind_ip = "0.0.0.0"
    bind_port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((bind_ip, bind_port))
    print(f"[Listening] {bind_ip}:{bind_port}")

    tDisplay = threading.Thread(target=displayThread)
    tDisplay.start()

    count = 0
    while True:
        data, addr = server.recvfrom(65535)
        q.put(data)
        # print(f"[Recv]{addr}: {data}")
        print(f"[Recv]{addr}: {count}")
        count += 1

if __name__ == '__main__':
    main()
