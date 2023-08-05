class VendorInfo:
    def __init__(self, vendor):
        self.__name = vendor.get("name")
        self.__modelName = vendor.get("modelName")
        self.__serialNo = vendor.get("serialNo")

    @property
    def name(self):
        return self.__name

    @property
    def modelName(self):
        return self.__modelName

    @property
    def serialNo(self):
        return self.__serialNo
