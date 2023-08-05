import json
import time
import urllib
import sys

from testwizard.testobjects_core import TestObjectBase

#Remote control commands
from testwizard.commands_remotecontrol import SendRCKeyCommand

#Power control commands
from testwizard.commands_powerswitch import GetPowerSwitchStatusCommand
from testwizard.commands_powerswitch import SwitchPowerCommand
from testwizard.commands_powerswitch import SwitchPowerOffCommand
from testwizard.commands_powerswitch import SwitchPowerOnCommand

#Audio commands
from testwizard.commands_audio import WaitForAudioCommand
from testwizard.commands_audio import WaitForPeakAudioCommand

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

class SetTopBox(TestObjectBase):
    def __init__(self, session, name):
        TestObjectBase.__init__(self, session, name, "STB")

    #Remote Control Commands
    def sendRCKey(self, keyName):
        self.throwIfDisposed()
        return SendRCKeyCommand(self).execute(keyName)

    #Power control commands
    def switchPower(self, on):
        self.throwIfDisposed()
        return SwitchPowerCommand(self).execute(on)
    
    def switchPowerOff(self):
        self.throwIfDisposed()
        return SwitchPowerOffCommand(self).execute()
    
    def switchPowerOn(self):
        self.throwIfDisposed()
        return SwitchPowerOnCommand(self).execute()
    
    def getPowerSwitchStatus(self):
        self.throwIfDisposed()
        return GetPowerSwitchStatusCommand(self).execute()

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
    
    def filterGrayscale(self, levels):
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
    
    def waitForSample(self, x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod = None, maxDistance = None):
        self.throwIfDisposed()
        return WaitForSampleCommand(self).execute(x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance)
    
    def waitForSampleNoMatch(self, x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod = None, maxDistance = None):
        self.throwIfDisposed()
        return WaitForSampleNoMatchCommand(self).execute(x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance)