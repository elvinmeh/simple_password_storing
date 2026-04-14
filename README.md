# simple_password_storing
Program for storing and managing passwords using Python program

My final work for HarvardX CS50x course! 

# ElvinPass — README Description

---

## What is ElvinPass?

ElvinPass is a **command-line password manager** built in Python, similar to KeePass. It allows users to securely store, retrieve, update, and delete passwords in a local encrypted SQLite database. It was developed as a CS50x final project in 2020.

---

## How it works

The program is built across three files:

**`elvinpass.py`** — Main entry point. Handles startup logic, argument parsing, and user authentication flow.

**`definitions.py`** — Core logic. Contains all functions for user management, password CRUD operations, and the interactive menu interface.

**`aes.py`** — Encryption engine. Handles AES-CBC encryption and decryption of stored passwords.

---

## Features

- **User authentication** — Username and password protected with `pbkdf2:sha512` hashing
- **AES encryption** — All stored passwords are encrypted using AES-CBC before being saved to the database
- **Two usage modes:**
  - **Interactive UI** — Menu-driven interface to manage password entries
  - **Command-line mode** — Directly retrieve a password by name and copy it to clipboard
- **Clipboard integration** — Decrypted passwords are copied directly to clipboard and never printed on screen
- **Root-only execution** — Script requires root privileges for security
- **SQLite storage** — All data stored locally in a `.db` file with `600` permissions

---

## Usage

```bash
# Interactive mode
python3 elvinpass.py mypasswords.db

# Command-line mode (copies password directly to clipboard)
python3 elvinpass.py mypasswords.db <username> <entry_name>

# Help
python3 elvinpass.py --help
```

---

## Dependencies

```
cs50
werkzeug
pycryptodome
pyperclip
```
