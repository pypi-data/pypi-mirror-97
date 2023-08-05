class RemoteControlInfo:
    def __init__(self, remoteControl):
        self.__isSupported = remoteControl.get("isSupported")
        self.__name = remoteControl.get("name")

    @property
    def isSupported(self):
        return self.__isSupported

    @property
    def name(self):
        return self.__name
