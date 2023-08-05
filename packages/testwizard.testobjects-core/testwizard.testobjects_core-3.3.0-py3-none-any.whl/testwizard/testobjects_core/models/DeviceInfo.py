from .VendorInfo import VendorInfo

class DeviceInfo:
    def __init__(self, device):
        self.__softwareVersion = device.get("softwareVersion")
        self.__hardwareVersion = device.get("hardwareVersion")
        self.__serialNo = device.get("serialNo")
        self.__vendor = VendorInfo(device.get("vendor"))
        self.__description = device.get("description")

    @property
    def softwareVersion(self):
        return self.__softwareVersion

    @property
    def hardwareVersion(self):
        return self.__hardwareVersion

    @property
    def serialNo(self):
        return self.__serialNo

    @property
    def vendor(self):
        return self.__vendor

    @property
    def description(self):
        return self.__description
