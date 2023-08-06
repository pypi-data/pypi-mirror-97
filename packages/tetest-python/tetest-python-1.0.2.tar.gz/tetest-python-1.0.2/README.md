# Information
TeTest-python is a plugin for user to build the connection to Te-Test testing platform.

## Table of Contents

- [Information](#information)
  - [Table of Contents](#table-of-contents)
  - [Publish](#publish)
  - [Install](#install)
    - [Configration](#configration)

## Publish
```sh
pip install .
python setup.py sdist build
sudo pip install twine
twine upload dist/*
```

## Install

[pip][]:

```sh
pip install tetest-python && pip freeze > requirements.txt
```

### Configration
```js
{
    "Server": "http://localhost:8080",
    "Token": "",
    "Project": "",
    "TaskID": "",
    "BuildID": "",
    "TimeSpan": "",
    "Paramerter": {},
    "TaskInfo": {},
    "JobInfo": {},
    "Data": [],
    "Report": {
        "ReportGroupName": "TeTest-LocalTest",
        "File": "report.xml",
        "Path": "/",
        "ImagePath": "webdriver_screenshots"
    },
    "Agent": "PYTEST"
}
```
