import win32gui
import win32ui
import win32con
import numpy
import cv2
from lib import utils
from lib import alerts
from threading import Thread, Timer

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
        print('Apex detected!')
        lookForApexTimer.cancel()
        detect_champion_selection()


def takeScreenshot(isJumpmaster):
    # https://answers.opencv.org/question/229026/help-with-optimization-opencv-python/
    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd == 0:
        print("Apex not found. Waiting for Apex to start...")
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

    print(
        f"Jumpmaster detected: {'true  ' if max_val >= 0.8 else 'false'} - {currentIteration}/{maxIteration}", end='\r', flush=True)

    currentIteration = currentIteration + 1
    if (max_val >= 0.8):
        soundThread = Thread(target=alerts.playRandomSound)
        discordThread = Thread(target=alerts.sendDiscordDM,
                               args=("DU BIST JUMPMASTER",))
        soundThread.start()
        discordThread.start()
        jumpmasterTimer.cancel()
        print()  # new line
        detect_champion_selection()
        currentIteration = 0
    elif(currentIteration == maxIteration):
        jumpmasterTimer.cancel()
        print()  # new line
        detect_champion_selection()
        currentIteration = 0


def detect_champion_selection():
    global champSelectTimer
    champSelectTimer = Timer(20, detect_champion_selection)
    champSelectTimer.start()
    max_val = getImgSimilarity(False)
    if max_val is None:
        return

    print(
        f"Champion selection detected: {'true  ' if max_val >= 0.8 else 'false'}")

    if max_val >= 0.8:
        champSelectTimer.cancel()
        print()  # new line
        detect_jumpmaster()


def cancelAllTimers():
    if champSelectTimer != '' and champSelectTimer.is_alive():
        champSelectTimer.cancel()
    if jumpmasterTimer != '' and jumpmasterTimer.is_alive():
        jumpmasterTimer.cancel()
    if lookForApexTimer != '' and lookForApexTimer.is_alive():
        lookForApexTimer.cancel()
