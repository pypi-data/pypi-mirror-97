import json
import urllib

from .models.TestObjectInfo import TestObjectInfo

#Services commands
from testwizard.commands_services import SendNotificationCommand

class TestObjectBase():
    def __init__(self, session, name, category):
        if session is None:
            raise Exception("Session is required")
        if name is None:
            raise Exception("Name is required")
        if category is None:
            raise Exception("Category is required")

        if session.robot is None:
            raise Exception("Robot is undefined for session")

        resources = session.metadata["resources"]
        for resource1 in resources:
            if resource1["name"] == name:
                resource = resource1
                break
            else:
                resource = None
        if resource is None:
            raise Exception("No resource found with name " + name)
        
        testobject = session.robot.getTestObject(resource["id"])
        self.info = TestObjectInfo(testobject)
        if "customProperties" in resource:
            self.customProperties = resource["customProperties"]
        else:
            self.customProperties = {}

        self.session = session
        self.name = name

        self.__isDisposed = False

    def executeCommand(self, commandName, requestObj, errorMessagePrefix):
        return self.session.robot.executeCommand(self.session.testRunId, self.name, commandName, requestObj, errorMessagePrefix)

    def dispose(self):
        self.__isDisposed = True

    def throwIfDisposed(self):
        if self.__isDisposed is True:
            print("Cannot access a disposed object")
            raise Exception("Cannot access a disposed object.")

    def sendNotification(self, errorId, description, priority):
        self.throwIfDisposed()
        return SendNotificationCommand(self).execute(errorId, description, priority)
        
    def setAttributeOnScreenDisplay(self, attributeType, osdArea,  textColor, backgroundColor, duration):
        self.throwIfDisposed()
        return SetAttributeOnScreenDisplayCommand(self).execute(attributeType, osdArea,  textColor, backgroundColor, duration)
        
    def setTextOnScreenDisplay(self, osdText, osdArea,  textColor, backgroundColor, duration):
        self.throwIfDisposed()
        return SetTextOnScreenDisplayCommand(self).execute(osdText, osdArea,  textColor, backgroundColor, duration)
        
    def clearOnScreenDisplay(self, osdArea):
        self.throwIfDisposed()
        return ClearOnScreenDisplayCommand(self).execute(osdArea)