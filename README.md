# Employee Onboarding System

This small local web app creates a personalized welcome email and onboarding guide from a few employee details. The app itself uses only Python's standard library. It does not need a database or an internet connection when you run it.

## Build and run on Windows

1. Install Python 3.10 or newer once from [python.org/downloads](https://www.python.org/downloads/). During setup, tick **Add python.exe to PATH**.
2. Double-click `build-windows.bat`. It creates a private build environment, downloads PyInstaller, and builds the app. Building needs an internet connection for that PyInstaller download.
3. Find the finished app at `dist\OnboardingSystem.exe`.
4. Double-click `OnboardingSystem.exe`. Your browser opens the onboarding form at `http://127.0.0.1:8080`. If that port is occupied, the app tries ports 8081 through 8090 and prints the address it uses.
5. To stop the app, close its console window or press **Ctrl+C** in that window.

You can share the single `OnboardingSystem.exe` with other Windows PCs. Those PCs do not need Python installed.

## Quick test without building

Double-click `run-windows.bat`, or open a terminal in this folder and run `python app.py` (or `py -3 app.py`). The app opens in your default browser.

## Run the tests

From this project folder, run:

```text
python -m unittest discover
```

## Troubleshooting

- **Python is not on PATH:** Rerun the Python installer and enable **Add python.exe to PATH**, then open a new terminal and run the build again.
- **Port 8080 is in use:** The app tries ports 8081 through 8090. Use the URL printed in the console.
- **SmartScreen or antivirus warns about the app:** This is an unsigned app you built locally. If you trust this project, choose **More info**, then **Run anyway**.
- **The build cannot download PyInstaller:** Building needs internet access. Connect to the internet and run `build-windows.bat` again. The finished app does not need internet to run.
- **The browser does not open:** Copy the URL printed in the console into your browser.
