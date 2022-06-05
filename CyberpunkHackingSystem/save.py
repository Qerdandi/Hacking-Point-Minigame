from cryptography.fernet import Fernet

class Save:
    def __init__(self):
        self.file_name = 'local_data.txt'
    
    def save_score(self, score):
        message = str(score).encode()  # .encode() is used to turn the string to bytes
        key = Fernet.generate_key()  # Store this key or get if you already have it
        encrypted = Fernet(key).encrypt(message)

        with open(self.file_name, 'wb') as file:
            file.write(key + "\n".encode() + encrypted) # Write the encrypted bytes to the output file

    def get_score(self):
        try:
            with open(self.file_name, 'rb') as file:
                data = file.read().split("\n".encode()) # Read the bytes of the encrypted file

            key = data[0]
            message = data[1]

            decrypted = Fernet(key).decrypt(message)
            return int(decrypted)
        except Exception:
            print("Invalid Key - Unsuccessfully decrypted")
        return 0