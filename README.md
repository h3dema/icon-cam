
## Install environment

### in Linux

Let's create an environment called `cam` to run our code.
The following lines create the environment using `pyenv`, activate it and install the dependencies.

```bash
pyenv virtualenv 3.11 cam
pyenv activate cam
pip install -r requirements.txt
```

To run the code use:

```bash
python cam.py
```

> **NOTE**: May not work on WSL2.

### in Windows

In Windows, you should use `pyenv` for Windows. Read more about the installation process [here](https://github.com/pyenv-win/pyenv-win).
The following lines create the environment in PowerShell, and activate it.

```bash
cd icon-cam
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```


### Packaging

Use pyinstaller to create a standalone exe file:

```bash
pyinstaller --onefile cam.py
```
