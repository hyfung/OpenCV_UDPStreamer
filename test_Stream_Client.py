from Stream_Client import *
import pytest
import time

def test_captureThread_hasVideoInput():
    return True

    tCapture = threading.Thread(target=captureThread, args=("test.mp4",))
    tCapture.start()

    # Wait for 5 seconds
    time.sleep(5)
    run = False

def test_captureThread_noVideoInput():
    # This should fail because no video input
    with pytest.raises(Exception):
        captureThread("test2.mp4")

def test_captureThread_noVideoInput():
    captureThread("test2.mp4")    


def test_sigint_handler():
    assert sigint_handler(signal.SIGINT, None) == True

