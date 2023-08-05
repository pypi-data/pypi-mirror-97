# Testwizard - Web

> Python language support for testing websites, web-apps or webservices using testwizard

## Usage

* Import the [testwizard.test](https://pypi.org/project/testwizard.test/) and the testwizard.web packages.
* Get a session and use it to create a web testobject.
* Use this object to execute commands.
* You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample script

### Python (website.js)

```Python
from testwizard.test import TestWizard
from testwizard.test import ResultCodes
from testwizard.web import Web

with TestWizard() as TW:
    session = TW.session

    print(f"param1 = {session.parameters['param1']}")
    print(f"param2 = {session.parameters['param2']}")

    website = Web(session, "TestwizardWebsite")

    print("startWebDriver")
    result = website.startWebDriver()
    print(result.message)
    if not result.success:
        session.addFail(result.message)
        exit()

    # Add your commands here

    print("quitDriver")
    result = website.quitDriver()
    print(result.message)
    if not result.success:
        session.addFail(result.message)

    if not (session.hasFails or session.hasErrors):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (website.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [{ "category": "WEB", "name": "TestwizardWebsite", "id": "Testwizard web site"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)
