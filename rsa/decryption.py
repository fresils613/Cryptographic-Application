from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os
from  hashlib import sha256
from pathlib import Path
from termcolor import cprint
from zip import Compress
import getpass

class Decryption:
    def File_decryption(self):
        cprint('Enter input the file name or path to decrypt (use / instead of \): ',end=' ', color='red', attrs=['bold','blink'])
        self.filename =input()
        

        new_file_name = os.path.basename(self.filename) # if the file name is a path, choose the last name of the path.
        file_in = open(self.filename, "rb")

        encrypted_file_text = 'decrypted_' + new_file_name # The name of decrypted file 
        encrypted_file_object = open(encrypted_file_text, 'wb')


        cprint('Please input the private key name or path plus the proper file extension (use / instead of \): ',end=' ', color='red', attrs=['bold','blink'])
        self.private = input()
        passphrase = getpass.getpass("Enter a passphrase for the private key: ")
        private_key = RSA.import_key(open(self.private).read(), passphrase=passphrase)

        #   PICKING THE APPROPRIATE INFORMATION FROM THE CIPHER FILE AND APPOINTING THEM TO THIER RESPECTIVE FOLDER
        enc_AES_key,nonce, tag,ciphertext = \
        [ file_in.read(x) for x in (private_key.size_in_bytes(),16,16,-1) ]
        # Decrypt the AES Key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        AES_key = cipher_rsa.decrypt(enc_AES_key)
        # Decrypt the data with the AES session key
        cipher_aes = AES.new(AES_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        encrypted_file_object.write(data)
        encrypted_file_object.close()

        # To decompress the file
        d = Compress()
        d.decompress(encrypted_file_text) 
        os.remove(encrypted_file_text)

    def Folder_decryption(self):
        cprint('Enter the encrypted folder path (use / instead of \): ',end=' ', color='red', attrs=['bold','blink'])
        self.Directory = input()
        cprint(f'Enter the private key name or path (use / instead of \): ',end=' ', color='red', attrs=['bold','blink'])
        self.private = input()
        passphrase = getpass.getpass("Enter a passphrase for the private key: ")

        # os.makedirs(self.dir_path, exist_ok=True)
        assert Path(self.Directory).is_dir()
        for new_path in sorted(Path(self.Directory).iterdir(), key=lambda p: str(p).lower()):
            with open(new_path, 'rb') as file_in:
                self.new_file_name = os.path.basename(new_path)   
                encrypted_file_text = 'decrypted_' + self.new_file_name
                self.private_key = RSA.import_key(open(self.private).read(), passphrase=passphrase)
                self.enc_AES_key,self.nonce, self.tag,self.ciphertext = \
                [file_in.read(x) for x in (self.private_key.size_in_bytes(),16,16,-1) ]

                # Decrypt the AES key with the private RSA key
                cipher_rsa = PKCS1_OAEP.new(self.private_key)
                AES_key = cipher_rsa.decrypt(self.enc_AES_key)
                # Decrypt the data with the AES session key
                cipher_aes = AES.new(AES_key, AES.MODE_EAX, self.nonce)
                data = cipher_aes.decrypt_and_verify(self.ciphertext, self.tag)
                encrypted_file_object = open(encrypted_file_text, 'wb')
                encrypted_file_object.write(data)
                encrypted_file_object.close()   

                d = Compress()
                d.decompress(encrypted_file_text)
                cprint('Decryption and Decompression  Done. Check the Directory you input for your Plain Text Text', color='green', attrs=['bold','blink'])       
                os.remove(encrypted_file_text)

