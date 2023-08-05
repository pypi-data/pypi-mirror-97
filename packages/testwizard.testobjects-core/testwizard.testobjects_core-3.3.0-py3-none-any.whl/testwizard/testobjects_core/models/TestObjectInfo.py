from .VideoInfo import VideoInfo
from .AudioInfo import AudioInfo
from .RemoteControlInfo import RemoteControlInfo
from .DeviceInfo import DeviceInfo
from .MobileInfo import MobileInfo

class TestObjectInfo:
    def __init__(self, testObject):
        self.__id = testObject.get("id")
        self.__name = testObject.get("name")
        self.__category = testObject.get("category")
        self.__isEnabled = testObject.get("isEnabled")
        self.__isLocked = testObject.get("isLocked")
        self.__video = VideoInfo(testObject.get("video"))
        self.__audio = AudioInfo(testObject.get("audio"))
        self.__remoteControl = RemoteControlInfo(testObject.get("remoteControl"))
        self.__device = DeviceInfo(testObject.get("device"))
        self.__mobile = MobileInfo(testObject.get("mobile") or {})

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def category(self):
        return self.__category

    @property
    def isEnabled(self):
        return self.__isEnabled

    @property
    def isLocked(self):
        return self.__isLocked

    @property
    def video(self):
        return self.__video

    @property
    def audio(self):
        return self.__audio

    @property
    def remoteControl(self):
        return self.__remoteControl

    @property
    def device(self):
        return self.__device

    @property
    def mobile(self):
        return self.__mobile