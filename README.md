# Employee Onboarding System

Generates a complete onboarding pack for a new hire from their name, role, department and start date: a welcome email, a 7-day plan, a documents checklist, an IT access checklist, FAQs and training resources. It runs locally on your own PC, uses no external services and needs no internet connection. The pack can be downloaded as a .txt email and a .md file.

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

## Troubleshooting

- **The page doesn't load:** the app tries port 8080 first, then 8081 to 8090. Check the black console window for the exact address it printed.
- **The black window closes straight away:** another copy may already be running, or the file was blocked. Run it from Command Prompt to see the error message.
- **"Python was not found" when building:** install Python from https://www.python.org/downloads/ and tick "Add python.exe to PATH". Ignore the Microsoft Store shortcut.
- **SmartScreen or antivirus warning:** the .exe is unsigned. Choose "More info", then "Run anyway".
