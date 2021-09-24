import win32gui
import win32ui
import win32con
import numpy
import cv2
from lib import utils
from lib import alerts

currentIteration = 1


def lookForApex(scheduler, hwnd):
    event = scheduler.enter(1, 1, lookForApex, (scheduler, hwnd))
    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd != 0:
        print('Apex detected!')
        scheduler.cancel(event)
        detect_champion_selection(scheduler)


def takeScreenshot(scheduler, isJumpmaster, event):
    # https://answers.opencv.org/question/229026/help-with-optimization-opencv-python/
    hwnd = win32gui.FindWindow(None, 'Apex Legends')
    if hwnd == 0:
        print("Apex not found. Waiting for Apex to start...")
        lookForApex(scheduler, hwnd)
        scheduler.cancel(event)
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


def getImgSimilarity(scheduler, isJumpmaster, event):
    screenshot_gray = takeScreenshot(scheduler, isJumpmaster, event)
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


def detect_jumpmaster(scheduler):
    global currentIteration
    maxIteration = 120

    event = scheduler.enter(1, 1, detect_jumpmaster, scheduler)

    max_val = getImgSimilarity(scheduler, True, event)

    print(
        f"Jumpmaster detected: {'true  ' if max_val >= 0.8 else 'false'} - {currentIteration}/{maxIteration}", end='\r', flush=True)

    currentIteration = currentIteration + 1
    if (max_val >= 0.8):
        alerts.playRandomSound()
        alerts.sendDiscordDM("DU BIST JUMPASTER")
        scheduler.cancel(event)
        print()  # new line
        detect_champion_selection(scheduler)
        currentIteration = 0
    elif(currentIteration == maxIteration):
        scheduler.cancel(event)
        print()  # new line
        detect_champion_selection(scheduler)
        currentIteration = 0


def detect_champion_selection(scheduler):
    event = scheduler.enter(20, 1, detect_champion_selection, scheduler)
    max_val = getImgSimilarity(scheduler, False, event)
    if max_val is None:
        return

    print(
        f"Champion selection detected: {'true  ' if max_val >= 0.8 else 'false'}")

    if max_val >= 0.8:
        scheduler.cancel(event)
        print()  # new line
        detect_jumpmaster(scheduler)
