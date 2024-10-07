import struct
import os
from Crypto.Cipher import AES
from hashlib import md5

# Helper function to generate MD5 checksum
def md5_checksum(data):
    return md5(data).digest()

# Helper function to pad data for AES-CBC (block size = 16)
def pad(data):
    padding_length = 16 - len(data) % 16
    return data + bytes([padding_length] * padding_length)

# Card parameters
signature = b'AGPAY'
version = b'01'
encryption_key = os.urandom(32)  # 32 bytes encryption key
reserved = b'\x00' * 10  # 10 bytes reserved
iv = os.urandom(16)  # 16 bytes IV
balance = 313371337  # The balance you want

# Create the unencrypted data (e.g., cardNumber, expiry date, balance)
card_number = b'1234567890123456'  # 16 bytes card number
expiry_date = struct.pack('>I', 1735689600)  # Example timestamp for expiration
balance_data = struct.pack('>Q', balance)  # Big-endian 64-bit unsigned integer

# Compose unencrypted data (total 32+ bytes)
decrypted_data = card_number + b'\x00\x00\x00\x00' + expiry_date + balance_data
decrypted_data = pad(decrypted_data)  # AES requires data length to be a multiple of 16

# Encrypt the data using AES-CBC
cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
encrypted_data = cipher.encrypt(decrypted_data)

# Footer and checksum
footer_signature = b'ENDAGP'
checksum = md5_checksum(iv + encrypted_data)

# Create the final card file content
card_content = (
    signature +
    version +
    encryption_key +
    reserved +
    iv +
    encrypted_data +
    footer_signature +
    checksum
)

# Save to a file
with open('newcard.agpay', 'wb') as f:
    f.write(card_content)

print("Card created with balance:", balance)