class VideoInfo:
    def __init__(self, video):
        self.__isSupported = video.get("isSupported")

    @property
    def isSupported(self):
        return self.__isSupported
