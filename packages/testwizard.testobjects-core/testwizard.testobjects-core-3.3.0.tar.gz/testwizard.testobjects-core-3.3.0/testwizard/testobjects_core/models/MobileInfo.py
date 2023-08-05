class MobileInfo:
    def __init__(self, mobile):
        self.__platformName = mobile.get("platformName")

    @property
    def platformName(self):
        return self.__platformName
