import rsa
from client import client_program
from server import server_program

def test_secure_communication():
    """Test the secure communication between client and server."""
    # Step 1: Server generates RSA keys
    server_pub_key, server_priv_key = rsa.newkeys(2048)

    # Step 2: Client generates encrypted AES key and message
    message = "This is a secret message from the client."
    encrypted_aes_key, encrypted_message = client_program(server_pub_key, message)

    # Step 3: Server decrypts the AES key and message
    decrypted_message = server_program(encrypted_aes_key, encrypted_message, server_priv_key)

    # Step 4: Verify the decrypted message matches the original
    print("Test Case 1: Secure Communication")
    print("Decrypted Message:", decrypted_message)
    assert decrypted_message == message, "Test Case 1 Failed"
    print("Test Case 1 Passed\n")

def test_large_message():
    """Test the secure communication with a large message."""
    # Step 1: Server generates RSA keys
    server_pub_key, server_priv_key = rsa.newkeys(2048)

    # Step 2: Client generates encrypted AES key and message
    large_message = "A" * 1000000  # 1 MB message
    encrypted_aes_key, encrypted_message = client_program(server_pub_key, large_message)

    # Step 3: Server decrypts the AES key and message
    decrypted_message = server_program(encrypted_aes_key, encrypted_message, server_priv_key)

    # Step 4: Verify the decrypted message matches the original
    print("Test Case 2: Large Message Handling")
    print("Decrypted Message Length:", len(decrypted_message))
    assert decrypted_message == large_message, "Test Case 2 Failed"
    print("Test Case 2 Passed\n")

def test_special_characters():
    """Test the secure communication with a message containing special characters."""
    # Step 1: Server generates RSA keys
    server_pub_key, server_priv_key = rsa.newkeys(2048)

    # Step 2: Client generates encrypted AES key and message
    special_message = "!@#$%^&*()_+{}:\"<>?[];',./`~"
    encrypted_aes_key, encrypted_message = client_program(server_pub_key, special_message)

    # Step 3: Server decrypts the AES key and message
    decrypted_message = server_program(encrypted_aes_key, encrypted_message, server_priv_key)

    # Step 4: Verify the decrypted message matches the original
    print("Test Case 3: Special Characters Handling")
    print("Decrypted Message:", decrypted_message)
    assert decrypted_message == special_message, "Test Case 3 Failed"
    print("Test Case 3 Passed\n")

def test_message_integrity():
    """Test the integrity of the message during communication."""
    # Step 1: Server generates RSA keys
    server_pub_key, server_priv_key = rsa.newkeys(2048)

    # Step 2: Client generates encrypted AES key and message
    original_message = "This message should remain intact."
    encrypted_aes_key, encrypted_message = client_program(server_pub_key, original_message)

    # Step 3: Simulate tampering with the encrypted message (e.g., flipping a bit)
    tampered_message = bytearray(encrypted_message)
    tampered_message[0] ^= 0x01  # Flip the first bit

    # Step 4: Server attempts to decrypt the tampered message
    try:
        decrypted_message = server_program(encrypted_aes_key, bytes(tampered_message), server_priv_key)
    except Exception as e:
        print("Test Case 4: Message Integrity Check")
        print("Decryption failed due to tampering:", str(e))
        print("Test Case 4 Passed\n")
        return

    # Step 5: Verify the decrypted message does not match the original
    print("Test Case 4: Message Integrity Check")
    print("Decrypted Message:", decrypted_message)
    assert decrypted_message != original_message, "Test Case 4 Failed: Tampered message decrypted successfully."
    print("Test Case 4 Passed\n")

if __name__ == "__main__":
    test_secure_communication()
    test_large_message()
    test_special_characters()
    test_message_integrity()