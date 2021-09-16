import cv2
import numpy
import mss
import sched, time

# https://stackoverflow.com/a/474543
s = sched.scheduler(time.time, time.sleep)

name = './images/jumpIcon.png' 
jumpmasterIcon = cv2.imread(name,0)

delayInSeconds = 0.5

def screen_record_efficient(sc):
    mon = {'left': 1100, 'top': 1076, 'width': 80, 'height': 80} # position of jumpmaster icon for 2560x1440 screens
    sct = mss.mss()

    img = numpy.asarray(sct.grab(mon))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, jumpmasterIcon, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    print(max_val)
    if max_val >= 0.8: 
        sendNotification()
   
    s.enter(delayInSeconds, 1, screen_record_efficient, (sc,))

s.enter(delayInSeconds, 1, screen_record_efficient, (s,))
s.run()

def sendNotification():
    playSound()
    showPopup()

def