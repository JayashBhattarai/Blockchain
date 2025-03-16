import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def generate_aes_key():
    """Generate a random 256-bit AES key."""
    return get_random_bytes(32)

def encrypt_aes_key(aes_key, rsa_pub_key):
    """Encrypt the AES key using the server's RSA public key."""
    return rsa.encrypt(aes_key, rsa_pub_key)

def encrypt_message(message, aes_key):
    """Encrypt a message using AES."""
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ct_bytes

def client_program(server_pub_key, message):
    """Simulate the client-side operations."""
    # Generate a random AES key
    aes_key = generate_aes_key()

    # Encrypt the AES key using the server's RSA public key
    encrypted_aes_key = encrypt_aes_key(aes_key, server_pub_key)

    # Encrypt the message using the AES key
    encrypted_message = encrypt_message(message, aes_key)

    return encrypted_aes_key, encrypted_message