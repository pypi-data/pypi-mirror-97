class AudioInfo:
    def __init__(self, audio):
        self.__isSupported = audio.get("isSupported")

    @property
    def isSupported(self):
        return self.__isSupported
