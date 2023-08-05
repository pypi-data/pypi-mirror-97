import json
import time
import urllib
import sys

from testwizard.testobjects_core import TestObjectBase

#Mobile commands
from testwizard.commands_mobile import InitDriverCommand
from testwizard.commands_mobile import QuitDriverCommand
from testwizard.commands_mobile import AddCapabilityCommand
from testwizard.commands_mobile import Android_SendKeyCodeCommand
from testwizard.commands_mobile import ClickElementCommand
from testwizard.commands_mobile import ClickPositionCommand
from testwizard.commands_mobile import CloseAppCommand
from testwizard.commands_mobile import RemoveAppCommand
from testwizard.commands_mobile import FindElementCommand
from testwizard.commands_mobile import GetElementAttributeCommand
from testwizard.commands_mobile import GetElementLocationCommand
from testwizard.commands_mobile import GetElementSizeCommand
from testwizard.commands_mobile import GetOrientationCommand
from testwizard.commands_mobile import GetScreenSizeCommand
from testwizard.commands_mobile import GetSourceCommand
from testwizard.commands_mobile import HideKeyboardCommand
from testwizard.commands_mobile import InputTextCommand
from testwizard.commands_mobile import LaunchAppCommand
from testwizard.commands_mobile import MultiTouch_AddCommand
from testwizard.commands_mobile import MultiTouch_NewCommand
from testwizard.commands_mobile import MultiTouch_PerformCommand
from testwizard.commands_mobile import PinchCoordinatesCommand
from testwizard.commands_mobile import PinchElementCommand
from testwizard.commands_mobile import ResetAppCommand
from testwizard.commands_mobile import RunAppInBackgroundCommand
from testwizard.commands_mobile import ScreenshotBMPCommand
from testwizard.commands_mobile import ScreenShotJPGCommand
from testwizard.commands_mobile import SetOrientationCommand
from testwizard.commands_mobile import StartDeviceLoggingCommand
from testwizard.commands_mobile import StopDeviceLoggingCommand
from testwizard.commands_mobile import SwipeCommand
from testwizard.commands_mobile import SwipeArcCommand
from testwizard.commands_mobile import TouchAction_MoveToCommand
from testwizard.commands_mobile import TouchAction_MoveToElementCommand
from testwizard.commands_mobile import TouchAction_NewCommand
from testwizard.commands_mobile import TouchAction_PerformCommand
from testwizard.commands_mobile import TouchAction_PressCommand
from testwizard.commands_mobile import TouchAction_PressElementCommand
from testwizard.commands_mobile import TouchAction_ReleaseCommand
from testwizard.commands_mobile import TouchAction_TapCommand
from testwizard.commands_mobile import TouchAction_WaitCommand
from testwizard.commands_mobile import WaitForElementCommand
from testwizard.commands_mobile import ZoomCoordinatesCommand
from testwizard.commands_mobile import ZoomElementCommand

#Video commands
from testwizard.commands_video import CaptureReferenceBitmapCommand
from testwizard.commands_video import CompareCommand
from testwizard.commands_video import CountLastPatternMatchesCommand
from testwizard.commands_video import DeleteAllRecordingsCommand
from testwizard.commands_video import DeleteAllSnapshotsCommand
from testwizard.commands_video import DetectMotionCommand
from testwizard.commands_video import DetectNoMotionCommand
from testwizard.commands_video import FilterBlackWhiteCommand
from testwizard.commands_video import FilterCBICommand
from testwizard.commands_video import FilterColorBlackWhiteCommand
from testwizard.commands_video import FilterGrayscaleCommand
from testwizard.commands_video import FilterInvertCommand
from testwizard.commands_video import FindAllPatternLocationsCommand
from testwizard.commands_video import FindAllPatternLocationsExCommand
from testwizard.commands_video import FindPatternCommand
from testwizard.commands_video import FindPatternExCommand
from testwizard.commands_video import GetVideoResolutionCommand
from testwizard.commands_video import LoadReferenceBitmapCommand
from testwizard.commands_video import SaveReferenceBitmapCommand
from testwizard.commands_video import SaveRegionCommand
from testwizard.commands_video import SetRegionCommand
from testwizard.commands_video import SnapShotBMPCommand
from testwizard.commands_video import SnapShotJPGCommand
from testwizard.commands_video import StartBackgroundCaptureCommand
from testwizard.commands_video import StartRecordingCommand
from testwizard.commands_video import StopBackgroundCaptureCommand
from testwizard.commands_video import StopRecordingCommand
from testwizard.commands_video import TextOCRCommand
from testwizard.commands_video import WaitForColorCommand
from testwizard.commands_video import WaitForColorNoMatchCommand
from testwizard.commands_video import WaitForPatternCommand
from testwizard.commands_video import WaitForPatternNoMatchCommand
from testwizard.commands_video import WaitForSampleCommand
from testwizard.commands_video import WaitForSampleNoMatchCommand

class Mobile(TestObjectBase):
    def __init__(self, session, name):
        TestObjectBase.__init__(self, session, name, "MOBILE")

    #Mobile commands
    def initDriver(self, appPath = None):
        self.throwIfDisposed()
        return InitDriverCommand(self).execute(appPath)
    
    def quitDriver(self):
        self.throwIfDisposed()
        return QuitDriverCommand(self).execute()

    def closeApp(self):
        self.throwIfDisposed()
        return CloseAppCommand(self).execute()    
    
    def addCapability(self, name, value):
        self.throwIfDisposed()
        return AddCapabilityCommand(self).execute(name, value)
    
    def android_SendKeyCode(self, keyCode):
        self.throwIfDisposed()
        return Android_SendKeyCodeCommand(self).execute(keyCode)
    
    def clickElement(self, selector):
        self.throwIfDisposed()
        return ClickElementCommand(self).execute(selector) 
    
    def clickPosition(self, x, y):
        self.throwIfDisposed()
        return ClickPositionCommand(self).execute(x, y) 
    
    def findElement(self, selector):
        self.throwIfDisposed()
        return FindElementCommand(self).execute(selector)
    
    def getElementAttribute(self, selector, attribute):
        self.throwIfDisposed()
        return GetElementAttributeCommand(self).execute(selector, attribute)    
    
    def getElementLocation(self, selector):
        self.throwIfDisposed()
        return GetElementLocationCommand(self).execute(selector)
    
    def getElementSize(self, selector):
        self.throwIfDisposed()
        return GetElementSizeCommand(self).execute(selector)   
    
    def getOrientation(self):
        self.throwIfDisposed()
        return GetOrientationCommand(self).execute()
    
    def getScreenSize(self):
        self.throwIfDisposed()
        return GetScreenSizeCommand(self).execute()   
    
    def getSource(self):
        self.throwIfDisposed()
        return GetSourceCommand(self).execute()
    
    def hideKeyboard(self, iOS_Key = None):
        self.throwIfDisposed()
        return HideKeyboardCommand(self).execute(iOS_Key)
    
    def inputText(self, selector, text):
        self.throwIfDisposed()
        return InputTextCommand(self).execute(selector, text)
    
    def launchApp(self):
        self.throwIfDisposed()
        return LaunchAppCommand(self).execute()
    
    def multiTouch_Add(self):
        self.throwIfDisposed()
        return MultiTouch_AddCommand(self).execute()   
    
    def multiTouch_New(self):
        self.throwIfDisposed()
        return MultiTouch_NewCommand(self).execute()     
    
    def multiTouch_Perform(self):
        self.throwIfDisposed()
        return MultiTouch_PerformCommand(self).execute()    
    
    def pinchCoordinates(self, x, y, length):
        self.throwIfDisposed()
        return PinchCoordinatesCommand(self).execute(x, y, length)    
    
    def pinchElement(self, selector):
        self.throwIfDisposed()
        return PinchElementCommand(self).execute(selector)
    
    def resetApp(self):
        self.throwIfDisposed()
        return ResetAppCommand(self).execute()

    def removeApp(self, appId):
        self.throwIfDisposed()
        return RemoveAppCommand(self).execute(appId)          
    
    def runAppInBackground(self, seconds = None):
        self.throwIfDisposed()
        return RunAppInBackgroundCommand(self).execute(seconds)
    
    def screenshotBMP(self, filename):
        self.throwIfDisposed()
        return ScreenshotBMPCommand(self).execute(filename)    
    
    def screenshotJPG(self, filename, quality):
        self.throwIfDisposed()
        return ScreenShotJPGCommand(self).execute(filename, quality)    
    
    def setOrientation(self, orientation):
        self.throwIfDisposed()
        return SetOrientationCommand(self).execute(orientation)
    
    def startDeviceLogging(self, filename, username = None, password = None):
        self.throwIfDisposed()
        return StartDeviceLoggingCommand(self).execute(filename, username, password)    
    
    def stopDeviceLogging(self):
        self.throwIfDisposed()
        return StopDeviceLoggingCommand(self).execute()    
    
    def swipe(self, startX, startY, endX, endY, duration):
        self.throwIfDisposed()
        return SwipeCommand(self).execute(startX, startY, endX, endY, duration)
    
    def swipeArc(self, centerX, centerY, radius, startDegree, degrees, steps):
        self.throwIfDisposed()
        return SwipeArcCommand(self).execute(centerX, centerY, radius, startDegree, degrees, steps)    
    
    def touchAction_MoveTo(self, x, y):
        self.throwIfDisposed()
        return TouchAction_MoveToCommand(self).execute(x, y)
    
    def touchAction_MoveToElement(self, selector):
        self.throwIfDisposed()
        return TouchAction_MoveToElementCommand(self).execute(selector)    
    
    def touchAction_New(self):
        self.throwIfDisposed()
        return TouchAction_NewCommand(self).execute()
    
    def touchAction_Perform(self):
        self.throwIfDisposed()
        return TouchAction_PerformCommand(self).execute()    
    
    def touchAction_Press(self, x, y):
        self.throwIfDisposed()
        return TouchAction_PressCommand(self).execute(x, y)    
    
    def touchAction_PressElement(self, selector):
        self.throwIfDisposed()
        return TouchAction_PressElementCommand(self).execute(selector)    
    
    def touchAction_Release(self):
        self.throwIfDisposed()
        return TouchAction_ReleaseCommand(self).execute()
    
    def touchAction_Tap(self, x, y):
        self.throwIfDisposed()
        return TouchAction_TapCommand(self).execute(x, y)
    
    def touchAction_Wait(self, duration):
        self.throwIfDisposed()
        return TouchAction_WaitCommand(self).execute(duration)    
    
    def waitForElement(self, selector, maxSeconds):
        self.throwIfDisposed()
        return WaitForElementCommand(self).execute(selector, maxSeconds)    
    
    def zoomCoordinates(self, x, y, length):
        self.throwIfDisposed()
        return ZoomCoordinatesCommand(self).execute(x, y, length)    
    
    def zoomElement(self, selector):
        self.throwIfDisposed()
        return ZoomElementCommand(self).execute(selector)

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
        return DetectMotionCommand(self).execute(x, y, width, height, minDifference, timeout, motionDuration, distanceMethod, minDistance)
    
    def detectNoMotion(self, x, y, width, height, minDifference, timeout, motionDuration = None, tolerance = None, distanceMethod = None, minDistance = None):
        self.throwIfDisposed()
        return DetectNoMotionCommand(self).execute(x, y, width, height, minDifference, timeout, motionDuration, distanceMethod, minDistance)
    
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