# Testwizard - Smart-Tv

> Python language support for testing Smart-Tv devices using testwizard

## Usage

* Import the [testwizard.test](https://pypi.org/project/testwizard.core/) and the testwizard.smart_tv packages
* Get a session and use it to create a Smart TV testobject.
* Use this object to execute commands.
* You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample script

### Python (smart-tv.py)

```python
from sys import path
path.append("../packages/test")
path.append("../packages/testobjects/core")
path.append("../packages/testobjects/smartTv")
path.append("../packages/commands/core")
path.append("../packages/commands/audio")
path.append("../packages/commands/powerswitch")
path.append("../packages/commands/remotecontrol")
path.append("../packages/commands/video")
path.append("../packages/commands/camera")

from testwizard.test import TestWizard
from testwizard.test import ResultCodes
from testwizard.smart_tv import SmartTv

with TestWizard() as TW:
    session = TW.session

    print("-- Parameter usage ---")
    print("  Param1 = " + session.parameters["param1"])
    print("  Param2 = " + session.parameters["param2"])

    print("-- Session info ---")
    print("  scriptFilePath = " + session.info["scriptFilePath"])
    print("  scriptFileName = " + session.info["scriptFileName"])
    print("  storagePath = " + session.info["storagePath"])
    print("  tester = " + session.info["tester"])
    print("  environment.scriptsBasePath = " + session.info["environment"]["scriptsBasePath"])
    print("  environment.storageBasePath = " + session.info["environment"]["storageBasePath"])
    print("  environment.ocrEngine = " + session.info["environment"]["ocrEngine"])
    print("  environment.testWizardVersion = " + session.info["environment"]["testWizardVersion"])

    if session.info["session"] is not None:
        print("Script was started by the Manager:")
        print("  session.id = " + session.info["session"]["id"])
        print("  session.name = " + session.info["session"]["name"])
        print("  session.scriptIndex = " + session.info["session"]["scriptIndex"])
    else:
        print("Script was started from the IDE")

    print("-- Create Smart TV test object ---")
    smartTv = SmartTv(session, "SmartTv")

    print("-- Smart TV test object info ---")
    print("  id = " + smartTv.info.id)
    print("  name = " + smartTv.info.name)
    print("  category = " + smartTv.info.category)
    print("  device.serialNo = " + smartTv.info.device.serialNo)
    print("  device.hardwareVersion = " + smartTv.info.device.hardwareVersion)
    print("  device.softwareVersion = " + smartTv.info.device.softwareVersion)
    print("  device.description = " + smartTv.info.device.description)
    print("  device.vendor.name = " + smartTv.info.device.vendor.name)
    print("  device.vendor.modelName = " + smartTv.info.device.vendor.modelName)
    print("  device.vendor.serialNo = " + smartTv.info.device.vendor.serialNo)

    print("-- Commands ---")

    basePath = session.info["environment"]["scriptsBasePath"]

    print("smartTV: cameraInitializeNetwork")
    result = smartTv.cameraInitializeNetwork()
    print(result.message)
    if result.success is False:
        print("Fail")
        session.addFail(result.message)

    snapShotFilePath = basePath + "smart-tv-py-test.jpg"

    print("smartTV: cameraSnapShot")
    result = smartTv.cameraSnapShot(snapShotFilePath)
    print(result.message)
    if result.success is False:
        print("Fail")
        session.addFail(result.message)

    motionX = 347
    motionY = 2
    motionWidth = 64
    motionHeight = 30
    motionDuration = 5
    motionDistanceThreshold = 10

    print("smartTV: cameraDetectMotion with motion - custom distanceThreshold")
    result = smartTv.cameraDetectMotion(motionX, motionY, motionWidth, motionHeight, motionDuration, motionDistanceThreshold)
    print(result.message)
    if result.success is False or not result.hasMotion:
        print("Fail")
        session.addFail(result.message)

    print("smartTV: cameraDetectMotion with motion - default distanceThreshold")
    result = smartTv.cameraDetectMotion(motionX, motionY, motionWidth, motionHeight, motionDuration)
    print(result.message)
    if result.success is False or result.hasMotion:
        print("Fail")
        session.addFail(result.message)

    print("smartTV: cameraDetectMotion with no motion - custom distanceThreshold")
    result = smartTv.cameraDetectMotion(motionX + 64, motionY, motionWidth, motionHeight, motionDuration, motionDistanceThreshold)
    print(result.message)
    if result.success is False or result.hasMotion:
        print("Fail")
        session.addFail(result.message)

    matchingReference = basePath + "Mibox_Home.bmp"
    nonMatchingReference = basePath + "Mibox_NotHome.bmp"
    roiX = 146
    roiY = 257
    roiWidth = 150
    roiHeight = 145
    sampleMatchDuration = 5
    sampleMatchDistanceThreshold = 21

    print("smartTV: cameraWaitForSampleNoMatch with no match - custom distanceThreshold")
    result = smartTv.loadReferenceBitmap(nonMatchingReference)
    print(result.message)
    if result.success is False:
        print("Fail")
        session.addFail(result.message)
    result = smartTv.cameraWaitForSampleNoMatch(roiX, roiY, roiWidth, roiHeight, sampleMatchDuration, sampleMatchDistanceThreshold)
    print(result.message)
    if result.success is False or result.hasMatch is True:
        print("Fail")
        session.addFail(result.message)

    print("smartTV: cameraWaitForSample with match - default distanceThreshold")
    result = smartTv.loadReferenceBitmap(matchingReference)
    print(result.message)
    if result.success is False:
        print("Fail")
        session.addFail(result.message)
    result = smartTv.cameraWaitForSample(roiX, roiY, roiWidth, roiHeight, sampleMatchDuration)
    print(result.message)
    if result.success is False or result.hasMatch is False:
        print("Fail")
        session.addFail(result.message)

    matchingPattern = basePath + "Mibox_Home_Pattern.bmp"
    patternX = 180
    patternY = 96
    patternWidth = 81
    patternHeight = 81
    patternMatchDuration = 5
    patternMatchDistanceThreshold = 21

    print("smartTV: cameraWaitForPattern with match - custom distanceThreshold")
    result = smartTv.cameraWaitForPattern(matchingPattern, patternX, patternY, patternWidth, patternHeight, patternMatchDuration, patternMatchDistanceThreshold)
    print(result.message)
    if result.success is False or result.hasMatch is False:
        print("Fail")
        session.addFail(result.message)

    nonMatchingPattern = basePath + "Mibox_NotHome_Pattern.bmp"

    print("smartTV: cameraWaitForPatternNoMatch with no match - default distanceThreshold")
    result = smartTv.cameraWaitForPatternNoMatch(nonMatchingPattern, patternX, patternY, patternWidth, patternHeight, patternMatchDuration)
    print(result.message)
    if result.success is False or result.hasMatch is True:
        print("Fail")
        session.addFail(result.message)

    if not (session.hasFails or session.hasErrors):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (smart-tv.json)

```json
{
    "tester": "John Smith",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [
        { "category": "SMART_TV", "name": "SmartTv", "id": "TV Model 1"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)