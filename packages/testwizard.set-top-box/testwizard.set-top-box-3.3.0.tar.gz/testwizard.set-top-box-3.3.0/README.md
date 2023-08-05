# Testwizard - set-top-box

> Python language support for testing set-top box devices using testwizard

## Usage

* Import the [testwizard.test](https://pypi.org/project/testwizard.test/) and the testwizard.set_top_box packages.
* Get a session and use it to create a set-top box testobject.
* Use this object to execute commands.
* You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample script

### Python (set-top-box.py)

```python
from testwizard.test import TestWizard
from testwizard.test import ResultCodes
from testwizard.set_top_box import SetTopBox

with TestWizard() as TW:
    session = TW.session

    print(f"param1 = {session.parameters['param1']}")
    print(f"param2 = {session.parameters['param2']}")

    setTopBox = SetTopBox(session, "SetTopBox")

    print("sendRCKey")
    result = setTopBox.sendRCKey("menu")
    print(result.message)
    if not result.success:
        session.addFail(result.message)

    if not (session.hasFails or session.hasErrors):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (set-top-box.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [{ "category": "STB", "name": "SetTopBox", "id": "SetTopBox 1"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)