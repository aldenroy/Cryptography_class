from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def main():
    # Read words from the file
    word_list = []
    with open('words.txt', 'r') as file:
        for line in file:
            new_line = line.strip()
            word_list.append(new_line)

    ciphertext_to_match = '8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9'
    plaintext_to_encrypt = 'This is a top secret.'

    found_key = None

    for word in word_list:
        if len(word) < 16:
            # Pad the word to 16 characters
            padded_word = word.ljust(16)

            # Convert the word and IV to bytes
            key = padded_word.encode('utf-8')
            iv = bytes(16)

            # Create a Cipher
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            # Encrypt the plaintext
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(plaintext_to_encrypt.encode()) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            # Check if the ciphertext matches the target
            if ciphertext.hex() == ciphertext_to_match:
                found_key = word
                break

    if found_key:
        print("A key was found, here is the key -->", found_key)
    else:
        print("No key exists.")

if __name__ == "__main__":
    main()
