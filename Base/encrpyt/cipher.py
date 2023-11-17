import base64
import uuid
from cryptography.fernet import Fernet



def generate_order_id():
    # Generate a unique identifier (UUID)
    unique_id = str(uuid.uuid4().int)

    # Get the current timestamp
    timestamp = int(time.time())

    # Combine the timestamp and the unique identifier
    order_id = f"ORDER-{timestamp}-{unique_id}"

    return order_id


def generate_key():
    """
    Generates a Fernet key and returns it.
    """
    key  = b'm9zlPa31JWfWqDvmgvEO56pSHjLmrfw1z9iHTiXj_z8='
    return key

def encrypt_message(message, key):
    """
    Encrypts a message using the provided key.
    Returns the encrypted message.
    """
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return encMessage

def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message using the provided key.
    Returns the decrypted message as a string.
    """
    fernet = Fernet(key)
    decMessage = fernet.decrypt(encrypted_message).decode()
    return decMessage

import random
import string
# Example usage:
def generate_random_id(length=12):
    characters = string.ascii_letters + string.digits  # Letters and digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def encode(id):
    return id.encode('utf-8')
def decode(id):
    decoded_value = id.decode('utf-8')
    return decoded_value
message = generate_random_id()
key = generate_key()
encrypted_message = encrypt_message('stark@gmail.com', key)
print(encrypted_message)
decrypted_message = decrypt_message('gAAAAABlNMUtDesYKBGIWHK82ciC3WC_5O1py9w8L-nCid4iE0LzOTDFkFRBFTO_owJ7Staly9ATfiv7MCdwUelXcpTXxzTiOQ==', key)
print(decrypted_message)