from Stream_Client import *

import time

def test_captureThread():
    tCapture = threading.Thread(target=captureThread, args=("test.mp4",))
    tCapture.start()

    # Wait for 5 seconds
    time.sleep(5)
    run = False
    # tCapture.join(1)

def test_captureThread_shouldFail():
    pass

def test_sigint_handler():
    assert sigint_handler(signal.SIGINT, None) == True

