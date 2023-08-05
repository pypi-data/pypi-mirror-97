# Testwizard - Core

> Python language support for testing different kinds of devices using testwizard

## Usage

Use this package in combination with one (or more) of the specific device packages

## Sidecar file

The testwizard manager enables a single script to be run on different devices with (optionally) different sets of parameters.
To enable this from any IDE a sidecar file (in json format) is used .
By default the name of the sidecar file is the same as this script, but with a .json extension.
A command-line-argument (--sidecar or -s) can be used to instruct the usage of a different file.

This json file has the following attributes:
* tester: The name of the tester (optional)
* parameters: An array of parameters (optional)
    * name: The name of the parameter
    * value: The value for the parameter
* resources: An array of resources
    * category: The category of the testobject
    * name: The name of the testobject
    * id: The id of the testobject
* outputFolder: The folder where the log files should be written (optional)

### Parameters

Every parameter will be made available as a field of the session object.

```python
    print('param1 = ' + session.parameters['param1'])
```

### Resources

All resources will be acquired (and thus locked) at the start of a test run and will be released when the script ends.
To execute a command on a testobject it must be referenced (constructed), when doing this, the name of the resource will be used, while the id corresponds to the actual device.

```python
    mobile = Mobile(session, "Mobile")
    result = mobile.initDriver()
```

### Output folder

When running a test all actions are logged (testrun.log) and so is the result (result.log).
By default the location of these files is a timestamp based folder within the runs folder.
If a different location is preferred, this can be configured in the outputfolder attribute.

## Session

When the script is executed (run or debug), a new session is created, and all resources will be locked
If any of the resources is allready in use, a session cannot be setup and an error will be thrown.
The session is destroyed when the script ends. At this point the resources will be released and available for other script runs.

More information about the session can be read from the info attribute:
* info
    * scriptFilePath: The full path of the script file
    * scriptFileName: The file name of the script file
    * storagePath: The directory where the output will be written
    * tester: The name of the tester
* info.environment
    * scriptsBasePath: The root directory where all scripts are stored
    * storageBasePath: The root directory where the output is written
    * ocrEngine: The name of the ocr engine being used
    * testWizardVersion: The version of testwizard being used
* info.session (optional: only when run from within the manager)
    * id: The unique identifier of the session in the manager
    * name: The name of the session
    * scriptIndex: The index of the script within the session

## Results

The outcome of a script run can be either Pass, Fail or Error.
During a script run multiple results can be reported, this can be done in 2 different ways:
1. addPass / addFail: reports a pass or fail but does not post it to the server
1. setResult: reports a pass / fail /error and posts it to the server

```python
    result = mobile.initDriver()
    if result.success:
        session.addPass(result.message)
    else:
        session.addFail(result.message)
```

```python
    result = mobile.initDriver()
    if result.success:
        session.setResult(ResultCodes.PASS, result.message)
    else:
        session.setResult(ResultCodes.FAIL, result.message)
```

## Sample script

### python (sample.py)

```python
import sys
import time

from testwizard.core import TestWizard
from testwizard.core import ResultCodes
from testwizard.mobile import Mobile
from testwizard.set_top_box import SetTopBox

with TestWizard() as TW:
    session = TW.session

    print("Parameters:")
    print("  param1 = " + session.parameters['param1'])
    print("  param2 = " + session.parameters['param2'])

    print("Session info:")
    print("  scriptFilePath = " + session.info["scriptFilePath"])
    print("  scriptFileName = " + session.info["scriptFileName"])
    print("  storagePath = " + session.info["storagePath"])
    print("  tester = " + session.info["tester"])
    print("  environment.scriptsBasePath = " + session.info["environment"]["scriptsBasePath"])
    print("  environment.storageBasePath = " + session.info["environment"]["storageBasePath"])
    print("  environment.ocrEngine = " + session.info["environment"]["ocrEngine"])
    print("  environment.testWizardVersion = " + session.info["environment"]["testWizardVersion"])
    if session.info["session"] is not None:
        print("Script was started by the manager:")
        print("  session.id = " + session.info["session"]["id"])
        print("  session.name = " + session.info["session"]["name"])
        print("  session.scriptIndex = " + session.info["session"]["scriptIndex"])

    mobile = Mobile(session, "Mobile")

    print("mobile: initDriver")
    result = mobile.initDriver()
    print(result.message)
    if result.success is False:
        session.addFail(result.message)

    setTopBox = SetTopBox(session, "STB")

    print("stb: sendRCKey")
    result = setTopBox.sendRCKey("menu")
    print(result.message)
    if result.success is False:
        session.addFail(result.message)

    if not (session.hasFails or session.hasErrors):
        session.addPass("Test was successful")
```
### sidecar file (sample.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [
        { "category": "MOBILE", "name": "Mobile", "id": "Mobile 1"},
        { "category": "STB", "name": "STB", "id": "SetTopBox 1"}
    ],
    "outputFolder": "c:\\temp"
}
```

## Compatibility

The version is compatible with testwizard version 3.1 - 3.4

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)