# CyberSafe Password Lab

A lightweight desktop password checker and generator built with Python and Tkinter. It gives local feedback on password strength and helps create stronger, unique passwords.

## Features

- **Live password analysis** with a strength score from 0 to 100 and a level: Weak, Fair, Good, or Excellent.
- **Actionable feedback** for password length, character variety, common passwords, predictable sequences, and repeated characters.
- **Secure password generation** using Python's `secrets` module, with a configurable length from 12 to 64 characters.
- **Show/hide password** control.
- **Copy to clipboard** control.
- **Local processing:** passwords are not sent to a server or saved by the app.

## Requirements

- Python 3.10 or later
- Tkinter (typically included with the standard Python installation)

No third-party Python packages are required.

## Run the application

Open a terminal in this project folder and run:

```bash
python password_checker_gui.py
```

On Windows, if `python` is not recognized, try:

```powershell
py password_checker_gui.py
```

## How to use

1. Type a password to see its strength score and suggestions update as you type.
2. Select **Show password** if you want to view the entered password.
3. Use **Generated password length** to select a length from 12 to 64.
4. Select **Generate secure password** to create a password containing lowercase letters, uppercase letters, digits, and symbols.
5. Select **Copy** to copy the current password to your clipboard.

## How the score works

The checker uses simple, local heuristics. It considers length, character groups, character variety, and a small set of common-password and predictable-pattern checks. The score is a learning aid, not a guarantee of security or a replacement for a password manager or a comprehensive password audit.

The generator uses Python's `secrets` module for cryptographically strong random choices. The app does not check passwords against online breach databases.

## Privacy and safety

Password analysis happens on your device. The app does not transmit or store passwords, but copying a password places it on your system clipboard. Clear the clipboard when you are finished, especially on a shared device.

Use a unique password for each account and store generated passwords in a trusted password manager.

## Project structure

```text
password_checker_gui.py   # Tkinter application
README.md                 # Project documentation
```

## License

No license has been specified yet. Add a `LICENSE` file before presenting this project as open source.
