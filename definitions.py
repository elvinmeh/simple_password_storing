import hashlib
from getpass import getpass
from werkzeug.security import check_password_hash, generate_password_hash
from Crypto.Cipher import AES
import re
import time
import pyperclip
import aes


def decrypt_and_copy_to_buffer_for_command(db, pass_name, user_pass):
    check = db.execute("SELECT name, pass FROM passwords WHERE name = :name", name=pass_name)
    if check:
        result = hashlib.md5(user_pass.encode())
        cipher = aes.AESCipher(result.hexdigest())
        decrypted_pass = cipher.decrypt(check[0]['pass'])
        pyperclip.copy(decrypted_pass)
        print("Password copied to clipboard.")
        time.sleep(3)


def decrypt_and_copy_to_buffer(encrypted_pass, user_pass):
    result = hashlib.md5(user_pass.encode())
    cipher = aes.AESCipher(result.hexdigest())
    decrypted_pass = cipher.decrypt(encrypted_pass)
    pyperclip.copy(decrypted_pass)
    print("Password copied to clipboard.")
    time.sleep(3)


def create_pass_entry(db, username, password):
    user_id = db.execute("SELECT id FROM users WHERE username = :username", username=username)[0]['id']
    print("\033c")
    name = input("Give name for entry: ")
    entry_pass = getpass("Type password for entry: ")
    result = hashlib.md5(password.encode())
    cipher = aes.AESCipher(result.hexdigest())
    encrypted_pass = cipher.encrypt(entry_pass)
    db.execute("INSERT INTO passwords (user_id, name, pass) VALUES (:user_id, :name, :entry_pass)",
               user_id=user_id, name=name, entry_pass=encrypted_pass)
    print("Entry successful saved!")
    time.sleep(2)


def update_entry(db, username, password, name):
    user_id = db.execute("SELECT id FROM users WHERE username = :username", username=username)[0]['id']
    new_name = input("Set new name (left blank for no changes): ")
    new_pass = getpass("Set new pass (left blank for no changes): ")
    if new_name != "":
        db.execute("UPDATE passwords SET name = :name_ WHERE user_id = :user_id AND name = :old_name",
                   user_id=user_id, name_=new_name, old_name=name)
        print("Entry name has been changed!\n")
    if new_pass != "":
        result = hashlib.md5(password.encode())
        cipher = aes.AESCipher(result.hexdigest())
        encrypted_pass = cipher.encrypt(new_pass)
        db.execute("UPDATE passwords SET pass = :password WHERE user_id = :user_id AND name = :name",
                   user_id=user_id, password=encrypted_pass, name=name)
        print("Password of entry has been changed!")
        time.sleep(2)


def delete_entry(db, username, name):
    answer = input("Are you sure? ")
    if re.search("(?i)y", answer) is not None:
        user_id = db.execute("SELECT id FROM users WHERE username = :username", username=username)[0]['id']
        db.execute("DELETE FROM passwords WHERE user_id = :user_id AND name = :name",
                   user_id=user_id, name=name)
        print("Successful deleted!\n")
        time.sleep(2)
        return True
    print("Deleting canceled!\n")
    time.sleep(2)
    return False


def there_is_users(db):
    try:
        checking = db.execute("SELECT * FROM users")
    except RuntimeError:
        return False
    return True


def create_user_and_table_in(db):
    username = input("Set username: ")
    password = getpass("Set password: ")
    password_hash = generate_password_hash(password, method='pbkdf2:sha512', salt_length=8)
    db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
               "'username' TEXT NOT NULL, 'hash' TEXT NOT NULL );")
    db.execute("CREATE TABLE IF NOT EXISTS 'passwords' ('user_id' INTEGER NOT NULL, 'name' TEXT NOT NULL, "
               "'pass' TEXT NOT NULL );")
    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
               username=username, hash=password_hash)
    return username, password


def authenticate_user(db, username, password):
    check = db.execute("SELECT hash FROM users WHERE username = :user", user=username)
    if not check or not check_password_hash(check[0]["hash"], password):
        return False
    else:
        return True


def starting_main_interface(db, username, password):
    check = db.execute("SELECT name, pass FROM passwords JOIN users ON id = user_id WHERE username = :username",
                       username=username)
    print("\033c")
    for var in range(len(check)):
        print(str(var+1) + ". " + check[var]['name'])
    print("\n")
    print("To copy: Type number and press Enter.")
    print("To delete: Type number and D (1d) and press Enter.")
    print("To update: Type number and U (1u) and press Enter.")
    print("To create a new one: Type C and press Enter.")
    print("For exit: Type E and press Enter.\n")
    answer = input("Choose your need: ")
    if re.search("^[0-9]$", answer) is not None and int(answer) - 1 in range(len(check)):
        decrypt_and_copy_to_buffer(check[int(answer) - 1]['pass'], password)
    elif re.search("(?i)^c$", answer) is not None:
        create_pass_entry(db, username, password)
    elif re.search("(?i)^[0-9]d$", answer) is not None and int(answer[0]) - 1 in range(len(check)):
        delete_entry(db, username, check[int(answer[0]) - 1]['name'])
    elif re.search("(?i)^[0-9]u$", answer) is not None and int(answer[0]) - 1 in range(len(check)):
        update_entry(db, username, password, check[int(answer[0]) - 1]['name'])
    elif re.search("(?i)^e$", answer) is not None:
        exit(0)
    else:
        print("Wrong choose")
    time.sleep(2)
