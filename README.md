# Keylogger Using Python with AES-GCM Encryption

A lightweight Python project that demonstrates keyboard-event capture, file logging, and AES-encrypted storage for defensive security research and authorized testing.

> ⚠️ This project is intended for authorized cybersecurity research only. Use it exclusively in a controlled lab or isolated virtual machine with explicit permission.

## Overview

This repository contains a simple Python-based keylogger prototype and an AES-GCM encryption utility.

- `mainfile.py` listens for keyboard input using `pynput` and writes captured keystrokes to a log file.
- `aes_encrypt_decrypt.py` provides AES-GCM encryption and decryption for log files.
- The logger automatically encrypts stored output when the `Esc` key is pressed.

## Features

- Keyboard event capture using `pynput`
- Plaintext log generation for local analysis
- Automatic log encryption on shutdown
- AES-GCM encryption with a password-derived key
- Command-line decryption support
- Simple setup for research and educational lab environments

## Project Structure

```text
ProjectKeylogger/
├── mainfile.py
├── aes_encrypt_decrypt.py
├── Keycodes.txt
├── requirements.txt
├── README.md
├── docs/
├── keylogs.txt
├── vvlogs.txt
├── *.enc
└── decrypted output files
```

## Requirements

- Python 3.9+
- Windows operating system
- `pynput`
- `cryptography`

## Installation

Clone the repository and install dependencies:

```powershell
git clone https://github.com/Vvarma8111/Python-Keylogger-With-AES-GCM-Encryption.git
cd Python-Keylogger-With-AES-GCM-Encryption
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

### 1. Start the keylogger

```powershell
python mainfile.py
```

The script begins capturing keystrokes and continues until `Esc` is pressed.

### 2. Encrypt the log automatically

When the listener is stopped, the program writes the captured data to a log file and encrypts it using AES-GCM.

### 3. Decrypt the log

```powershell
python aes_encrypt_decrypt.py decrypt -i vvlogs.txt.enc -o vvlogs_decrypted.txt
```

If a custom password was used, decrypt with:

```powershell
python aes_encrypt_decrypt.py decrypt -i vvlogs.txt.enc -o vvlogs_decrypted.txt --password YourPasswordHere
```

## Security and Ethics

This project is designed for defensive cybersecurity education and controlled research in authorized lab contexts.

Before use:

- Obtain explicit permission for the target environment.
- Run only in an isolated VM or sandbox.
- Do not use on personal, corporate, or non-consented systems.
- Replace hard-coded credentials with secure environment-managed secrets.
- Follow all local laws, institutional policies, and ethical guidelines.

## Disclaimer

This project is provided for educational and authorized research use only. It is not intended for unauthorized monitoring, invasive testing, or malicious activity.

## License

This repository does not include a formal software license file. Use it only under the terms of your organization's policies and applicable legal requirements.

## Summary

This repository demonstrates a minimal workflow for keyboard capture, log management, and encrypted persistence for controlled defensive research and security analysis.
