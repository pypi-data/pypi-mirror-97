# Testwizard - Android set-top-box

> Python language support for testing Android set-top box devices using testwizard

## Usage

* Import the [testwizard.test](https://pypi.org/project/testwizard.test/) and the testwizard.android_set_top_box packages.
* Get a session and use it to create an Android set-top box testobject.
* Use this object to execute commands.
* You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample script

### Python (android-set-top-box.py)

```python
from testwizard.test import TestWizard
from testwizard.test import ResultCodes
from testwizard.android_set_top_box import AndroidSetTopBox

with TestWizard() as TW:
    session = TW.session

    print(f"param1 = {session.parameters['param1']}")
    print(f"param2 = {session.parameters['param2']}")

    setTopBox = AndroidSetTopBox(session, "SetTopBox")

    print("sendRCKey")
    result = setTopBox.sendRCKey("menu")
    print(result.message)
    if not result.success:
        session.addFail(result.message)

    if not (session.hasFails or session.hasErrors):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (android-set-top-box.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [{ "category": "ANDROID_STB_TV", "name": "SetTopBox", "id": "SetTopBox 1"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)