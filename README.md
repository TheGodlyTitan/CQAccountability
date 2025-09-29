# **CQ Accountability Email Generator**

## **Overview**

The CQ Accountability Email Generator is a simple application, built with Python and Tkinter designed to streamline the process of creating the end-of-shift accountability email for Airman Leaders (ALs) and other CQ personnel. It provides a structured graphical interface (GUI) to input shift data, validate mandatory fields, and generate a correctly formatted, copy-and-paste ready email body for dissemination to command and MTLs.

## **Features**

- **Manor Selection:** Easily select between Winters or Fosters manor.
- **CQ Team:** Dedicated fields for all required CQ roles
- **Lates Tracking:** Dynamic entry sections for:
    - **Red-Card Lates**
    - **Standard Lates**
- **Automatic MTL Lookup:** Automatically determines the appropriate Bay MTL for accountability based on the entered room number and selected manor.
- **Notes Section:** Fields for CAC scanner status, On-Call MTL, and additional shift notes.
- **Required Signature Block:** Enforces input for all professional military signature fields.
- **Clipboard Functionality:**  Generates the email body in a separate window with a one-click copy button.

## **Download**

You have two options to run the Accountability Email Formatter:

### 1. Pre-Built Executables
- All compiled `.exe` releases are available in the [`/releases/`](./releases) directory.
- When running for the first time on Windows, **Microsoft Defender SmartScreen** may warn:
  > "Windows protected your PC – Unknown Publisher"
- This happens because the `.exe` is not code-signed. It is safe to run if downloaded from this repository.  
- To continue: click **More info → Run anyway**.
- (Optional) Advanced users may run the app with a [self-signed certificate](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signed-code) if they wish to remove the "Unknown publisher" message.

### 2. Run from Source
- Clone or download this repo.
```bash
pip install git+https://github.com/TheGodlyTitan/CQAccountability.git
```
- Install Python 3.10+.
- Run `app.py`
