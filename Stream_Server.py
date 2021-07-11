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

def displayThread():
    while run:
        data = q.get()
        tmp = np.asarray(bytearray(data), dtype='uint8')
        img = cv2.imdecode(tmp, cv2.IMREAD_COLOR)
        cv2.imshow("Receiving Feed", img)
        cv2.waitKey(100)

def main():
    # Attach a SIGINT handler to modify the global variable 'run'
    signal.signal(signal.SIGINT, sigint_handler)

    # Placeholder for 
    img = None

    # Configuration used locally, should've used argparse to take in arguments
    bind_ip = "0.0.0.0"
    bind_port = 9999

    # Create our server UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((bind_ip, bind_port))
    print(f"[Listening] {bind_ip}:{bind_port}")

    # Start our display thread
    tDisplay = threading.Thread(target=displayThread)
    tDisplay.start()

    count = 0
    while run:
        data, addr = server.recvfrom(65535)
        q.put(data)
        print(f"[Recv]{addr}: {count}")
        count += 1

    # Wait for display thread to gracefully exit
    tDisplay.join()

if __name__ == '__main__':
    main()
