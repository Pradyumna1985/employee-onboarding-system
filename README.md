## Download (Windows)

1. Go to the [Releases page](https://github.com/Pradyumna1985/employee-onboarding-system/releases) and download **OnboardingSystem.exe** under Assets.
2. Double-click it. A black console window opens and the app loads in your browser at http://localhost:8080.
3. Enter the employee's name, role, department and start date, then click generate.
4. To stop the app, close the black console window.

No Python or internet connection is needed to run the `.exe`.

**Windows SmartScreen warning:** the file is unsigned, so Windows may show a warning. Click **More info**, then **Run anyway**. Some antivirus tools also flag unsigned `.exe` files by mistake.

## Build from source

You need Python 3.10 or newer, installed with "Add python.exe to PATH" ticked.

1. Download or clone this repository.
2. Double-click `build-windows.bat`. The first run needs internet to download PyInstaller.
3. Your app appears at `dist\OnboardingSystem.exe`.

To run it without building, double-click `run-windows.bat`. To run the tests, use `py -m unittest discover`.
