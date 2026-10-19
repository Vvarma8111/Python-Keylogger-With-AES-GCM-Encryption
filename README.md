readme_content = """# Endpoint Input Monitoring & Defensive Analysis Research

## Project Overview
This repository contains the research codebase, cryptographic storage routines, and threat evaluation reports developed as an independent cybersecurity capstone research project. It investigates user-mode input capture mechanics, AES symmetric encryption at rest, antivirus heuristic detection boundaries, and endpoint defense engineering.

## Repository Contents
- `mainfile.py`: Core asynchronous input-monitoring script utilizing low-level OS hooks.
- `aes_encrypt_decrypt.py`: Symmetric cryptographic engine for AES encryption and decryption verification.
- `requirements.txt`: Frozen list of runtime dependencies.
- `docs/`: Formal academic reports, threat analyses, and presentation decks.

## Laboratory Environment Setup
Execution must occur strictly inside an isolated virtual machine:
1. Clone or extract this repository into your isolated workspace.
2. Initialize and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1