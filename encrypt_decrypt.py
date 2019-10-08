import base64
import os
import argparse
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# CLI Menu option
welcome = "Help details for encrypt_decrypt.py, which includes options to create a key and encrypt/decrypt a file."
parser = argparse.ArgumentParser(description=welcome)
parser.add_argument('-e', '--encrypt', help='Option for selecting and encrypting a file.')
parser.add_argument('-d', '--decrypt', help='Option for selecting and decrypting a file.')
parser.parse_args()

args = parser.parse_args()

print("************************************** ")
print(" Homework 3 - Encryption / Decryption ")
print(" Dillon Torgersen ")
print(" 10687846 ")
print("************************************** ")
print(" ")

# Gathers password input
password_provided = getpass.getpass("Provide password to create key: ")
password = password_provided.encode()

# Creates key to be used for encryption
salt = b'pF\xcc\x7f8\xc3LL8\xcf.t\xcf\x15\x0f\xb7'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

file = open('userkey.key','wb')
file.write(key)
file.close()

file = open('userkey.key','rb')
key = file.read()
file.close()

if args.encrypt:
	# File variables
	input_file = args.encrypt
	output_file = input_file+'.encrypted'

	# Open the file to encrypt: 
	with open(input_file,'rb') as f:
	    data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.encrypt(data)

	# Write the encrypted file:  
	with open(output_file,'wb') as f:
	    f.write(encrypted)

	os.remove('userkey.key')
	print("File encrypted successfully.")

elif args.decrypt:
	# Encrypted variables
	encrypted_input_file = args.decrypt
	encrypted_output_file = input("Name decrypted file: ")
	# Open encrypted file to decrypt:
	with open (encrypted_input_file, 'rb') as f:
	    data = f.read()

	fernet = Fernet(key)
	encrypted = fernet.decrypt(data)
	# Write the decrypted file:
	with open (encrypted_output_file, 'wb') as f:
		f.write(encrypted)

	os.remove('userkey.key')
	print("File decrypted successfully.")

print(" ")