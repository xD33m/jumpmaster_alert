import win32gui
import win32ui
import win32con
import numpy
import cv2
from lib import utils
from lib import alerts
from threading import Thread, Timer
from lib import sockets

currentIteration = 1

jumpmasterTimer = ''
champSelectTimer = ''
lookForApexTimer = ''


def lookForApex(hwnd):
    global lookForApexTimer
    lookForApexTimer = Timer(1, lookForApex, (hwnd,))
    lookForApexTimer.start()
    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd != 0:
        sockets.emitEvent("logs", 'Apex detected!')
        lookForApexTimer.cancel()
        sockets.resetDetection()
        detect_champion_selection()


def takeScreenshot(isJumpmaster):
    # https://answers.opencv.org/question/229026/help-with-optimization-opencv-python/
    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd == 0:
        sockets.emitEvent("logs",
                          "Apex not found. Waiting for Apex to start...")
        lookForApex(hwnd)
        if champSelectTimer != '' and champSelectTimer.is_alive():
            champSelectTimer.cancel()
        if jumpmasterTimer != '' and jumpmasterTimer.is_alive():
            jumpmasterTimer.cancel()

        return None
    imgPosition = utils.getNeedlePostion(isJumpmaster)

    imgLeft = imgPosition['left']
    imgTop = imgPosition['top']
    imgWidth = imgPosition['width']
    imgHeight = imgPosition['height']

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()

    saveBitMap.CreateCompatibleBitmap(mfcDC, imgWidth, imgHeight)
    saveDC.SelectObject(saveBitMap)

    saveDC.BitBlt((0, 0), (imgWidth, imgHeight), mfcDC,
                  (imgLeft, imgTop), win32con.SRCCOPY)
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    screenshot = numpy.frombuffer(signedIntsArray, dtype='uint8')
    screenshot.shape = (imgHeight, imgWidth, 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    screenshot_gray = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_BGR2GRAY)
    return screenshot_gray


def getImgSimilarity(isJumpmaster):
    screenshot_gray = takeScreenshot(isJumpmaster)
    if screenshot_gray is None:
        return None

    needleImgPath = utils.getNeedleImgPath(isJumpmaster)
    imgToCompare = cv2.imread(needleImgPath, 0)

    res = cv2.matchTemplate(
        screenshot_gray, imgToCompare, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # cv2.imshow("Image", img_gray)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('Fenster wird geschlossen')
    return max_val


def detect_jumpmaster():
    global currentIteration
    global jumpmasterTimer
    jumpmasterTimer = Timer(1, detect_jumpmaster)
    jumpmasterTimer.start()
    maxIteration = 120

    max_val = getImgSimilarity(True)

    # sockets.emitEvent("detection_log", {
    #     "jumpDetection": True, "charDetection": False})

    currentIteration = currentIteration + 1
    if (max_val >= 0.8):
        notifcationThread = Thread(target=alerts.sendNotification,
                                   args=("DU BIST JUMPMASTER",))
        notifcationThread.start()
        jumpmasterTimer.cancel()
        # sockets.emitEvent("detection_log", {
        #                   "jumpDetection": False, "charDetection": True})
        # sockets.emitDetectionEvent(championDetection=True)
        detect_champion_selection()
        currentIteration = 0

    elif(currentIteration == maxIteration):
        jumpmasterTimer.cancel()
        detect_champion_selection()
        currentIteration = 0
        # sockets.emitEvent("detection_log", {"status": "end"})
        # TODO: Hier noch ein emit senden?


def detect_champion_selection():
    print("Champion selection detection started")
    if(win32gui.FindWindow(None, 'Apex Legends') != 0):
        sockets.emitDetectionEvent(championDetection=True)
    global champSelectTimer
    champSelectTimer = Timer(1, detect_champion_selection)
    champSelectTimer.start()
    max_val = getImgSimilarity(False)
    if max_val is None:
        return

    if max_val >= 0.8:
        champSelectTimer.cancel()
        # sockets.emitEvent("detection_log", {
        #                   "jumpDetection": True, "charDetection": False})
        sockets.emitDetectionEvent(jumpmasterDetection=True)
        detect_jumpmaster()


def cancelAllTimers():
    if champSelectTimer != '' and champSelectTimer.is_alive():
        champSelectTimer.cancel()
    if jumpmasterTimer != '' and jumpmasterTimer.is_alive():
        jumpmasterTimer.cancel()
    if lookForApexTimer != '' and lookForApexTimer.is_alive():
        lookForApexTimer.cancel()
