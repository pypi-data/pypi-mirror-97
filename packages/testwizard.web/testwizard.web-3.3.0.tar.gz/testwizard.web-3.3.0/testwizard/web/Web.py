import json
import time
import urllib
import sys

from testwizard.testobjects_core import TestObjectBase

#Audio commands
from testwizard.commands_audio import WaitForAudioCommand
from testwizard.commands_audio import WaitForPeakAudioCommand

#Web Commands
from testwizard.commands_web.AcceptAlertCommand import AcceptAlert
from testwizard.commands_web.AddArgumentCommand import AddArgument
from testwizard.commands_web.AddChromeExtensionCommand import AddChromeExtension
from testwizard.commands_web.AuthenticateUrlCommand import AuthenticateUrl
from testwizard.commands_web.ClearCommand import Clear
from testwizard.commands_web.ClickCommand import Click
from testwizard.commands_web.DeleteAllCookiesCommand import DeleteAllCookies
from testwizard.commands_web.DismissAlertCommand import DismissAlert
from testwizard.commands_web.DragNDropCommand import DragNDrop
from testwizard.commands_web.GetChildrenCommand import GetChildren
from testwizard.commands_web.GetCurrentWindowHandleCommand import GetCurrentWindowHandle
from testwizard.commands_web.GetElementCommand import GetElement
from testwizard.commands_web.GetElementAttributeCommand import GetElementAttribute
from testwizard.commands_web.GetUrlCommand import GetUrl
from testwizard.commands_web.GetWindowHandlesCommand import GetWindowHandles
from testwizard.commands_web.GoToUrlCommand import GoToUrl
from testwizard.commands_web.IsDriverLoadedCommand import IsDriverLoaded
from testwizard.commands_web.MaximizeWindowCommand import MaximizeWindow
from testwizard.commands_web.MultiAction_ClickCommand import MultiAction_Click
from testwizard.commands_web.MultiAction_ClickAndHoldCommand import MultiAction_ClickAndHold
from testwizard.commands_web.MultiAction_ContextClickCommand import MultiAction_ContextClick
from testwizard.commands_web.MultiAction_DoubleClickCommand import MultiAction_DoubleClick
from testwizard.commands_web.MultiAction_DragAndDropCommand import MultiAction_DragAndDrop
from testwizard.commands_web.MultiAction_DragAndDropToOffsetCommand import MultiAction_DragAndDropToOffset
from testwizard.commands_web.MultiAction_keyDownCommand import MultiAction_keyDown
from testwizard.commands_web.MultiAction_keyUpCommand import MultiAction_keyUp
from testwizard.commands_web.MultiAction_MoveToElementCommand import MultiAction_MoveToElement
from testwizard.commands_web.MultiAction_MoveToElementOffsetCommand import MultiAction_MoveToElementOffset
from testwizard.commands_web.MultiAction_NewCommand import MultiAction_New
from testwizard.commands_web.MultiAction_PerformCommand import MultiAction_Perform
from testwizard.commands_web.MultiAction_ReleaseCommand import MultiAction_Release
from testwizard.commands_web.MultiAction_SendKeysCommand import MultiAction_SendKeys
from testwizard.commands_web.OpenInNewTabCommand import OpenInNewTab
from testwizard.commands_web.OpenInNewWindowCommand import OpenInNewWindow
from testwizard.commands_web.QuitDriverCommand import QuitDriver
from testwizard.commands_web.ScreenshotBMPCommand import ScreenshotBMP
from testwizard.commands_web.ScreenshotJPGCommand import ScreenshotJPGCommand
from testwizard.commands_web.ScrollByCommand import ScrollBy
from testwizard.commands_web.SendKeyboardShortcutCommand import SendKeyboardShortcut
from testwizard.commands_web.SendKeysCommand import SendKeys
from testwizard.commands_web.SendKeysAlertCommand import SendKeysAlert
from testwizard.commands_web.StartWebDriverCommand import StartWebDriver
from testwizard.commands_web.SubmitCommand import Submit
from testwizard.commands_web.SwitchToFrameCommand import SwitchToFrame
from testwizard.commands_web.SwitchToWindowCommand import SwitchToWindow
from testwizard.commands_web.WaitForControlCommand import WaitForControl

#Video commands
from testwizard.commands_video import GetVideoResolutionCommand
from testwizard.commands_video import CompareCommand
from testwizard.commands_video import CountLastPatternMatchesCommand
from testwizard.commands_video import FilterBlackWhiteCommand
from testwizard.commands_video import FilterCBICommand
from testwizard.commands_video import FilterColorBlackWhiteCommand
from testwizard.commands_video import FilterGrayscaleCommand
from testwizard.commands_video import FilterInvertCommand
from testwizard.commands_video import FindAllPatternLocationsCommand
from testwizard.commands_video import FindAllPatternLocationsExCommand
from testwizard.commands_video import FindPatternCommand
from testwizard.commands_video import FindPatternExCommand
from testwizard.commands_video import SetRegionCommand
from testwizard.commands_video import TextOCRCommand
from testwizard.commands_video import CaptureReferenceBitmapCommand
from testwizard.commands_video import DeleteAllRecordingsCommand
from testwizard.commands_video import DeleteAllSnapshotsCommand
from testwizard.commands_video import DetectMotionCommand
from testwizard.commands_video import DetectNoMotionCommand
from testwizard.commands_video import LoadReferenceBitmapCommand
from testwizard.commands_video import SaveReferenceBitmapCommand
from testwizard.commands_video import SaveRegionCommand
from testwizard.commands_video import SnapShotBMPCommand
from testwizard.commands_video import SnapShotJPGCommand
from testwizard.commands_video import StartBackgroundCaptureCommand
from testwizard.commands_video import StartRecordingCommand
from testwizard.commands_video import StopBackgroundCaptureCommand
from testwizard.commands_video import StopRecordingCommand
from testwizard.commands_video import WaitForColorCommand
from testwizard.commands_video import WaitForColorNoMatchCommand
from testwizard.commands_video import WaitForPatternCommand
from testwizard.commands_video import WaitForPatternNoMatchCommand
from testwizard.commands_video import WaitForSampleCommand
from testwizard.commands_video import WaitForSampleNoMatchCommand


class Web(TestObjectBase):
    def __init__(self, session, name):
        TestObjectBase.__init__(self, session, name, "WEB")

    #Web Commands
    def acceptAlert(self):
        self.throwIfDisposed()
        return AcceptAlert(self).execute()
    
    def addArgument(self, argument):
        self.throwIfDisposed()
        return AddArgument(self).execute(argument)
    
    def addChromeExtension(self, filePath):
        self.throwIfDisposed()
        return AddChromeExtension(self).execute(filePath)
    
    def authenticateUrl(self, username, password, link):
        self.throwIfDisposed()
        return AuthenticateUrl(self).execute(username, password, link)
    
    def clear(self, selector):
        self.throwIfDisposed()
        return Clear(self).execute(selector)
    
    def click(self, selector):
        self.throwIfDisposed()
        return Click(self).execute(selector)
    
    def deleteAllCookies(self):
        self.throwIfDisposed()
        return DeleteAllCookies(self).execute()
    
    def dismissAlert(self):
        self.throwIfDisposed()
        return DismissAlert(self).execute()
    
    def dragNDrop(self, object, target):
        self.throwIfDisposed()
        return DragNDrop(self).execute(object, target) 
    
    def getChildren(self, selector):
        self.throwIfDisposed()
        return GetChildren(self).execute(selector)
    
    def getCurrentWindowHandle(self):
        self.throwIfDisposed()
        return GetCurrentWindowHandle(self).execute()      
    
    def getElement(self, selector):
        self.throwIfDisposed()
        return GetElement(self).execute(selector)   
    
    def getElementAttribute(self, selector, name):
        self.throwIfDisposed()
        return GetElementAttribute(self).execute(selector, name)
    
    def getUrl(self):
        self.throwIfDisposed()
        return GetUrl(self).execute()
    
    def getWindowHandles(self):
        self.throwIfDisposed()
        return GetWindowHandles(self).execute()
    
    def goToUrl(self, url):
        self.throwIfDisposed()
        return GoToUrl(self).execute(url)
    
    def isDriverLoaded(self):
        self.throwIfDisposed()
        return IsDriverLoaded(self).execute()
    
    def maximizeWindow(self):
        self.throwIfDisposed()
        return MaximizeWindow(self).execute()
    
    def multiAction_Click(self, selector):
        self.throwIfDisposed()
        return MultiAction_Click(self).execute(selector)
    
    def multiAction_ClickAndHold(self, selector):
        self.throwIfDisposed()
        return MultiAction_ClickAndHold(self).execute(selector)
    
    def multiAction_ContextClick(self, selector):
        self.throwIfDisposed()
        return MultiAction_ContextClick(self).execute(selector)
    
    def multiAction_DoubleClick(self, selector):
        self.throwIfDisposed()
        return MultiAction_DoubleClick(self).execute(selector)
    
    def multiAction_DragAndDrop(self, sourceSelector, targetSelector):
        self.throwIfDisposed()
        return MultiAction_DragAndDrop(self).execute(sourceSelector, targetSelector)
    
    def multiAction_DragAndDropToOffset(self, selector, targetXOffset, targetYOffset):
        self.throwIfDisposed()
        return MultiAction_DragAndDropToOffset(self).execute(selector, targetXOffset, targetYOffset)
    
    def multiAction_KeyDown(self, key, selector = None):
        self.throwIfDisposed()
        return MultiAction_keyDown(self).execute(key, selector)
    
    def multiAction_KeyUp(self, key, selector = None):
        self.throwIfDisposed()
        return MultiAction_keyUp(self).execute(key, selector)
    
    def multiAction_MoveToElement(self, selector):
        self.throwIfDisposed()
        return MultiAction_MoveToElement(self).execute(selector)
    
    def multiAction_MoveToElementOffset(self, selector, xOffset, yOffset):
        self.throwIfDisposed()
        return MultiAction_MoveToElementOffset(self).execute(selector, xOffset, yOffset)
    
    def multiAction_New(self):
        self.throwIfDisposed()
        return MultiAction_New(self).execute()
    
    def multiAction_Perform(self):
        self.throwIfDisposed()
        return MultiAction_Perform(self).execute()
    
    def multiAction_Release(self, selector = None):
        self.throwIfDisposed()
        return MultiAction_Release(self).execute(selector)

    def multiAction_SendKeys(self, inputString, selector = None):
        self.throwIfDisposed()
        return MultiAction_SendKeys(self).execute(inputString, selector)

    def openInNewTab(self, selector):
        self.throwIfDisposed()
        return OpenInNewTab(self).execute(selector)
    
    def openInNewWindow(self, selector):
        self.throwIfDisposed()
        return OpenInNewWindow(self).execute(selector)
    
    def quitDriver(self):
        self.throwIfDisposed()
        return QuitDriver(self).execute()
    
    def screenshotBMP(self, filename):
        self.throwIfDisposed()
        return ScreenshotBMP(self).execute(filename)
    
    def screenshotJPG(self, filename, quality):
        self.throwIfDisposed()
        return ScreenshotJPGCommand(self).execute(filename, quality)
    
    def scrollBy(self, x, y):
        self.throwIfDisposed()
        return ScrollBy(self).execute(x, y)
    
    def sendKeyboardShortcut(self, selector, keys):
        self.throwIfDisposed()
        return SendKeyboardShortcut(self).execute(selector, keys)
    
    def sendKeys(self, selector, text):
        self.throwIfDisposed()
        return SendKeys(self).execute(selector, text)
    
    def sendKeysAlert(self, text):
        self.throwIfDisposed()
        return SendKeysAlert(self).execute(text)
    
    def startWebDriver(self, browser = None, serverUrl = None):
        self.throwIfDisposed()
        return StartWebDriver(self).execute(browser, serverUrl)
    
    def submit(self, selector):
        self.throwIfDisposed()
        return Submit(self).execute(selector)
    
    def switchToFrame(self, selector):
        self.throwIfDisposed()
        return SwitchToFrame(self).execute(selector)
    
    def switchToWindow(self, selector):
        self.throwIfDisposed()
        return SwitchToWindow(self).execute(selector)
    
    def waitForControl(self, selector, seconds):
        self.throwIfDisposed()
        return WaitForControl(self).execute(selector, seconds)

    #Audio Commands
    def waitForAudio(self, level, timeout):
        self.throwIfDisposed()
        return WaitForAudioCommand(self).execute(level, timeout)
    
    def waitForPeakAudio(self, level, timeout):
        self.throwIfDisposed()
        return WaitForPeakAudioCommand(self).execute(level, timeout)

    #Video Commands
    def captureReferenceBitmap(self):
        self.throwIfDisposed()
        return CaptureReferenceBitmapCommand(self).execute()
    
    def getVideoResolution(self):
        self.throwIfDisposed()
        return GetVideoResolutionCommand(self).execute()
    
    def compare(self, x, y, width, height, filename, tolerance):
        self.throwIfDisposed()
        return CompareCommand(self).execute(x, y, width, height, filename, tolerance)
    
    def countLastPatternMatches(self, similarity):
        self.throwIfDisposed()
        return CountLastPatternMatchesCommand(self).execute(similarity)
    
    def filterBlackWhite(self, separation):
        self.throwIfDisposed()
        return FilterBlackWhiteCommand(self).execute(separation)
    
    def filterCBI(self, contrast, brightness, intensity):
        self.throwIfDisposed()
        return FilterCBICommand(self).execute(contrast, brightness, intensity)
    
    def filterColorBlackWhite(self, color, tolerance):
        self.throwIfDisposed()
        return FilterColorBlackWhiteCommand(self).execute(color, tolerance)
    
    def filterGrayscaleCommand(self, levels):
        self.throwIfDisposed()
        return FilterGrayscaleCommand(self).execute(levels)
    
    def filterInvert(self):
        self.throwIfDisposed()
        return FilterInvertCommand(self).execute()
    
    def findAllPatternLocations(self, filename, mode, similarity):
        self.throwIfDisposed()
        return FindAllPatternLocationsCommand(self).execute(filename, mode, similarity)
    
    def findAllPatternLocationsEx(self, filename, mode, similarity, x, y, width, height):
        self.throwIfDisposed()
        return FindAllPatternLocationsExCommand(self).execute(filename, mode, similarity, x, y, width, height)
    
    def findPattern(self, filename, mode):
        self.throwIfDisposed()
        return FindPatternCommand(self).execute(filename, mode)
    
    def findPatternEx(self, filename, mode, x, y, width, height):
        self.throwIfDisposed()
        return FindPatternExCommand(self).execute(filename, mode, x, y, width, height)
    
    def setRegion(self, x, y, width, height):
        self.throwIfDisposed()
        return SetRegionCommand(self).execute(x, y, width, height)
    
    def textOCR(self, dictionary):
        self.throwIfDisposed()
        return TextOCRCommand(self).execute(dictionary)
    
    def deleteAllRecordings(self):
        self.throwIfDisposed()
        return DeleteAllRecordingsCommand(self).execute()
    
    def deleteAllSnapshots(self):
        self.throwIfDisposed()
        return DeleteAllSnapshotsCommand(self).execute()
    
    def detectMotion(self, x, y, width, height, minDifference, timeout, motionDuration = None, tolerance = None, distanceMethod = None, minDistance = None):
        self.throwIfDisposed()
        return DetectMotionCommand(self).execute(x, y, width, height, minDifference, timeout, motionDuration, tolerance, distanceMethod, minDistance)
    
    def detectNoMotion(self, x, y, width, height, minDifference, timeout, motionDuration = None, tolerance = None, distanceMethod = None, minDistance = None):
        self.throwIfDisposed()
        return DetectNoMotionCommand(self).execute(x, y, width, height, minDifference, timeout, motionDuration, tolerance, distanceMethod, minDistance)
    
    def loadReferenceBitmap(self, filename):
        self.throwIfDisposed()
        return LoadReferenceBitmapCommand(self).execute(filename)
    
    def saveReferenceBitmap(self, filename):
        self.throwIfDisposed()
        return SaveReferenceBitmapCommand(self).execute(filename) 
    
    def saveRegion(self, filename):
        self.throwIfDisposed()
        return SaveRegionCommand(self).execute(filename)
    
    def snapShotBMP(self, filename):
        self.throwIfDisposed()
        return SnapShotBMPCommand(self).execute(filename)
    
    def snapShotJPG(self, filename, quality):
        self.throwIfDisposed()
        return SnapShotJPGCommand(self).execute(filename, quality)
    
    def startBackgroundCapture(self, stepSize, captures):
        self.throwIfDisposed()
        return StartBackgroundCaptureCommand(self).execute(stepSize, captures)
    
    def startRecording(self, filename):
        self.throwIfDisposed()
        return StartRecordingCommand(self).execute(filename)
    
    def stopBackgroundCapture(self):
        self.throwIfDisposed()
        return StopBackgroundCaptureCommand(self).execute()
    
    def stopRecording(self):
        self.throwIfDisposed()
        return StopRecordingCommand(self).execute()
    
    def waitForColor(self, x, y, width, height, refColor, tolerance, minSimilarity, timeout):
        self.throwIfDisposed()
        return WaitForColorCommand(self).execute(x, y, width, height, refColor, tolerance, minSimilarity, timeout)
    
    def waitForColorNoMatch(self, x, y, width, height, refColor, tolerance, minSimilarity, timeout):
        self.throwIfDisposed()
        return WaitForColorNoMatchCommand(self).execute(x, y, width, height, refColor, tolerance, minSimilarity, timeout)
    
    def waitForPattern(self, filename, minSimilarity, timeout, mode, x, y, width, height):
        self.throwIfDisposed()
        return WaitForPatternCommand(self).execute(filename, minSimilarity, timeout, mode, x, y, width, height)
    
    def waitForPatternNoMatch(self, filename, minSimilarity, timeout, mode, x, y, width, height):
        self.throwIfDisposed()
        return WaitForPatternNoMatchCommand(self).execute(filename, minSimilarity, timeout, mode, x, y, width, height)
    
    def WaitForSample(self, x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod = None, maxDistance = None):
        self.throwIfDisposed()
        return WaitForSampleCommand(self).execute(x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance)
    
    def WaitForSampleNoMatch(self, x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod = None, maxDistance = None):
        self.throwIfDisposed()
        return WaitForSampleNoMatchCommand(self).execute(x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance)