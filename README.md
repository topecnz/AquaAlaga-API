# AquaAlaga Raspberry Pi

## Pre-requisite

- Python 3.11
- MongoDB

## Installation

To download the requirements, enter the following command:

```bash
pip install -r requirements.txt
```
Then, run the application:

```bash
python -m uvicorn main:app
```

## Contribution

To contribute this application, please enter the following commands:

### Linux
```bash
$ pip install pipenv
$ python -m venv .venv
$ source .venv/bin/activate
$ pipenv install
$ python -m uvicorn main:app
```

### Windows
```powershell
PS> pip install pipenv
PS> python -m venv .venv
PS> .venv\Scripts\activate
PS> pipenv install
PS> python -m uvicorn main:app
```