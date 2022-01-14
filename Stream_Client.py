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
    return (run == False)

def captureThread(source = 0):
    global run
    cap = cv2.VideoCapture(source)
    while run:
        ret, img = cap.read()
        img = cv2.resize(img, (320,240))
        ret, img_encode = cv2.imencode('.jpg', img)
        q.put(img_encode.tobytes())
        cv2.imshow("Transmitting Feed", img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            run = False
    return

def main():
    # Attach a SIGINT handler to modify the global variable 'run'
    signal.signal(signal.SIGINT, sigint_handler)

    # Configuration used locally, should've used argparse to take in arguments
    bind_ip = "0.0.0.0"
    bind_port = 9999

    # Create our UDP client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Start capturing frames
    tCapture = threading.Thread(target=captureThread)
    tCapture.start()

    count = 0
    while run:
        client.sendto(q.get(), (bind_ip, bind_port))
        time.sleep(0.1)
        print(f'[Send] {count}')
        count += 1

    # Wait for capture thread to gracefully exit
    tCapture.join()

if __name__ == '__main__':
    main()
