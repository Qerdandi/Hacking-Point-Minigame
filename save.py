from cryptography.fernet import Fernet

class Save:
    def __init__(self):
        self.file_name = 'local_data.txt'
    
    def save_data(self, data):
        message = b''
        encrypted = []
        key = Fernet.generate_key() # generate a key to encrypte data
        
        for i in range(len(data)): # for each data value
            message = str(data[i]).encode() # converting the data value in string and the data (message) in bytes 
            encrypted.append(Fernet(key).encrypt(message)) # use the key and Fernet method to encrypte the message

        with open(self.file_name, 'wb') as file:
            file.write(key + "\n".encode()) # write the encrypted bytes (key) to the output file and return line
            for i in range(len(data)):
                file.write(encrypted[i] + "\n".encode()) # write the encrypted bytes (data) to the output file and return line

    def get_data(self, index):
        try:
            with open(self.file_name, 'rb') as file:
                data = file.read().split("\n".encode()) # read the bytes of the encrypted file

            key = data[0]
            message = data[index]

            decrypted = Fernet(key).decrypt(message) # use the key and Fernet method to decrypt the message
            return int(decrypted) # return the decrypted message converted in int
        except Exception:
            print("Invalid Key - Unsuccessfully decrypted")
        return 0