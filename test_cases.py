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

if __name__ == "__main__":
    test_secure_communication()
    test_large_message()