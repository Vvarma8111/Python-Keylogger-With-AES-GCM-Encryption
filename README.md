# NewtonAI Endpoint Input Monitoring & Defensive Analysis Research

## Project Overview
This repository contains the research codebase, cryptographic storage routines, and threat evaluation reports developed as part of the NewtonAI Technologies Research Project. It investigates user-mode input capture mechanics, AES symmetric encryption at rest, antivirus heuristic detection boundaries, and endpoint defense engineering.

## Repository Contents
- mainfile.py: Core asynchronous input-monitoring script utilizing low-level OS hooks.
- aes_encrypt_decrypt.py: Symmetric cryptographic engine for AES encryption and decryption verification.
- requirements.txt: Frozen list of runtime dependencies.
- docs/: Formal academic reports, threat analyses, and presentation decks.

## Laboratory Environment Setup
Execution must occur strictly inside an isolated virtual machine:
1. Clone or extract this repository into your isolated workspace.
2. Initialize and activate a Python virtual environment:
   python -m venv venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
3. Install project dependencies:
   pip install -r requirements.txt

## Usage Syntax
- Run the research script in your isolated lab:
  python mainfile.py
- To test symmetric file encryption or decryption verification:
  python aes_encrypt_decrypt.py

## Statutory & Ethical Disclaimer
This tool and its associated documentation are created strictly for educational, defensive, and authorized academic research purposes. Deploying unauthorized keystroke interception tools violates domestic and international cybersecurity laws, including:
- India: Information Technology Act, 2000 (Sections 43, 66, and 69A) and the DPDP Act, 2023.
- United States: Computer Fraud and Abuse Act (CFAA, 18 U.S.C. § 1030) and the ECPA.
- European Union: General Data Protection Regulation (GDPR) Regulation (EU) 2016/679.

The authors and NewtonAI assume no liability for misuse, unauthorized execution, or damages resulting from this software.
