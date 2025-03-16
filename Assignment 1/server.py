import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_aes_key(encrypted_aes_key, rsa_priv_key):
    """Decrypt the AES key using the server's RSA private key."""
    return rsa.decrypt(encrypted_aes_key, rsa_priv_key)

def decrypt_message(encrypted_message, aes_key):
    """Decrypt a message using AES."""
    iv = encrypted_message[:AES.block_size]
    ct = encrypted_message[AES.block_size:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

def server_program(encrypted_aes_key, encrypted_message, server_priv_key):
    """Simulate the server-side operations."""
    # Decrypt the AES key using the server's RSA private key
    aes_key = decrypt_aes_key(encrypted_aes_key, server_priv_key)

    # Decrypt the message using the AES key
    decrypted_message = decrypt_message(encrypted_message, aes_key)

    return decrypted_message