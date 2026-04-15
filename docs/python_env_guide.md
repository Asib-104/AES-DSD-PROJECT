# Python Environment Guide

This project includes Python test scripts (`scripts/aes_encrypt.py` and `scripts/aes_decrypt.py`) for generating and verifying AES-128 encryptions and decryptions. To run the scripts, you'll need to set up a Python Virtual Environment (`venv`) to ensure that project dependencies (like `pycryptodome`) are isolated to this project. 

Follow the guide below based on your operating system. Both macOS and Windows setups are covered.

## Prerequisites

Make sure you have Python 3 installed. You can check this by running the following command in your terminal/command prompt:
```bash
python --version
# OR
python3 --version
```

---

## MacOS / Linux Instructions

**1. Create the Virtual Environment**
Open your terminal, navigate to the root folder of this project (`AES-DSD-PROJECT`), and run:
```bash
python3 -m venv venv
```
*(This command creates a new folder named `venv` containing the isolated Python interpreter.)*

**2. Activate the Environment**
```bash
source venv/bin/activate
```
*(You will see `(venv)` prepended to your command prompt, indicating it is active).*

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the Scripts**

*To Encrypt:*
```bash
python scripts/aes_encrypt.py
```

*To Decrypt:*
```bash
python scripts/aes_decrypt.py
```

**5. Deactivate (When Done)**
```bash
deactivate
```

---

## Windows Instructions

**1. Create the Virtual Environment**
Open Command Prompt or PowerShell, navigate to the root folder of this project (`AES-DSD-PROJECT`), and run:
```cmd
python -m venv venv
```
*(If `python` is not recognized, try `py -m venv venv`)*

**2. Activate the Environment**

*Using Command Prompt:*
```cmd
venv\Scripts\activate.bat
```

*Using PowerShell:*
```powershell
.\venv\Scripts\Activate.ps1
```
> **Note:** If PowerShell gives an Execution Policy error, run this command once as Administrator: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`, then try activating again.

**3. Install Dependencies**
```cmd
pip install -r requirements.txt
```

**4. Run the Scripts**

*To Encrypt:*
```cmd
python scripts\aes_encrypt.py
```

*To Decrypt:*
```cmd
python scripts\aes_decrypt.py
```

**5. Deactivate (When Done)**
```cmd
deactivate
```
