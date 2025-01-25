from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print(key)
generate_key()

def load_key():
    return open("secret.key", "rb").read()
key=load_key()
fernet = Fernet(key)

with open("Romantics essay.pdf", "rb") as original_file:
    original= original_file.read()

encrypted = fernet.encrypt(original)

with open ('enc_Romantics_essay.pdf', "wb") as encrypted_file:
    encrypted_file.write(encrypted)

 