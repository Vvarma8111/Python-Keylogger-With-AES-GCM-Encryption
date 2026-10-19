from aes_encrypt_decrypt import decrypt_file

ENCRYPTED_LOG = "keylogs.txt.enc"
DECRYPTED_LOG = "keylogs_decrypted.txt"
PASSWORD = "Varma@8135"


if __name__ == '__main__':
    decrypt_file(ENCRYPTED_LOG, DECRYPTED_LOG, password=PASSWORD)
    print(f"Decrypted file created: {DECRYPTED_LOG}")
    print(f"Password: {PASSWORD}")
