from cryptography.fernet import Fernet

class Save:
    def __init__(self):
        self.file_name = 'local_data.txt'
    
    def save_data(self, data):
        message = b''
        encrypted = []
        key = Fernet.generate_key()  # Store this key or get if you already have it
        
        for i in range(len(data)):
            message = str(data[i]).encode()
            encrypted.append(Fernet(key).encrypt(message))

        with open(self.file_name, 'wb') as file:
            file.write(key + "\n".encode()) # Write the encrypted bytes to the output file
            for i in range(len(data)):
                file.write(encrypted[i] + "\n".encode())

    def get_data(self, index):
        try:
            with open(self.file_name, 'rb') as file:
                data = file.read().split("\n".encode()) # Read the bytes of the encrypted file

            key = data[0]
            message = data[index]

            decrypted = Fernet(key).decrypt(message)
            return int(decrypted)
        except Exception:
            print("Invalid Key - Unsuccessfully decrypted")
        return 0