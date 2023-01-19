import os
import sys
from pathlib import Path
import os 
from termcolor import cprint
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from zip import Compress
from  hashlib import sha256

class Folder_Encryption:
    def folder_encryption(self):
        try:
            cprint('Enter the folder path your wish to encrypts (use / instead of \ ): ',end=' ', color='blue', attrs=['bold','blink'])
            self.Directory = input()
        except (IOError, FileNotFoundError):
            cprint('There is an error with the directory: ',end=' ', color='red', attrs=['bold','blink'])
            sys.exit(0)
        try:
            cprint('Enter the Directory Path you wish to save your encrypted Files (use / instead of \ ):  ',end=' ', color='blue', attrs=['bold','blink'])
            self.dir_path = input()
        except (IOError, FileNotFoundError): # Enter if there is any error with the filename/directory name
            cprint('There is a problem with the {self.dir_path} path.'.format(self.filename), color='red',attrs=['bold','blink']) # It is used to give the error color red.
            sys.exit(0) # Terminate the code
        cprint('Please enter the recepient public key file name or path with the correct file extention (use / instead of \ ):  ',end=' ', color='blue', attrs=['bold','blink'])
        self.receiver = input()
        os.makedirs(self.dir_path, exist_ok=True)
        assert Path(self.Directory).is_dir()
        for new_path in sorted(Path(self.Directory).iterdir(), key=lambda p: str(p).lower()):
            with open(new_path, 'rb') as p:
                cprint('This is for file {0}'.format(os.path.basename(new_path)), color='green', attrs=['bold','blink']) 
                hashh = 'Hash_' + os.path.basename(new_path)
                with open(new_path,'rb') as f: # Open the file to read it's bytes
                    file_hash = sha256() # Create the hash object, can use something other than `.sha256()` if you wish
                    fb = f.read() # Read from the file. Take in the amount declared above
                    while len(fb) > 0: # While there is still data being read from the file
                        file_hash.update(fb) # Update the hash
                        fb = f.read() # Read the next block from the file
                    # os.makedirs(self.dir_path, exist_ok=True)
                    if os.path.isfile(hashh):
                        with open(hashh, 'r') as h:
                            previous_hash = h.read()
                            if previous_hash == file_hash.hexdigest():
                                cprint('Already hashed, No new modification', color='red', attrs=['bold','blink'])
                            else:
                                #Compressing the file
                                c = Compress()
                                c.compress(new_path)
                                # Opening the file
                                cprint('Compression Done. Time for encryption ', color='green', attrs=['bold','blink'])   
                                encrypted_path_text = 'cipher_' + os.path.basename(new_path) #Add cipher to the name of the file                   
                                recipient_key = RSA.import_key(open(self.receiver).read()) # Public Key of the receiver 
                                AES_key_generate = get_random_bytes(32) # Generating the AES key which is in 128bits (i6bytes to bit)

                                rsa_cipher = PKCS1_OAEP.new(recipient_key) 
                                enc_AES_key = rsa_cipher.encrypt(AES_key_generate) # Using the recipient public key to encrypt the Aes Key

                                compress_file = 'compress_' + os.path.basename(new_path)
                                original_message = open(compress_file, 'rb')
                                textFile = original_message.read() # Reading the Plaintext File
                                textFile = bytearray(textFile) # Converting the content of the file to bit

                                aes_cipher = AES.new(AES_key_generate, AES.MODE_EAX)
                                ciphertext, tag = aes_cipher.encrypt_and_digest(textFile) # Encrypting thr file and generating the Cipher text and the hash digest(hash function)
                                encrypted_path_object = open(os.path.join(self.dir_path,encrypted_path_text), 'wb') # opening the file just created 
                                [ encrypted_path_object.write(x) for x in (enc_AES_key, aes_cipher.nonce, tag, ciphertext) ] # Storing our result in a file
                                with open(hashh, 'w') as h:
                                    h.write(file_hash.hexdigest())
                                encrypted_path_object.close() 
                                original_message.close()
                                cprint('Encryption Done. Check the Directory you input for your Cipher Text', color='green', attrs=['bold','blink']) 
                    else:                  
                        #Compressing the file
                        c = Compress()
                        c.compress(new_path)
                        # Opening the file
                        cprint('Compression Done. Time for encryption ', color='green', attrs=['bold','blink'])   
                        encrypted_path_text = 'cipher_' + os.path.basename(new_path)  #Add cipher to the name of the file                   
                        recipient_key = RSA.import_key(open(self.receiver).read()) # Public Key of the receiver 
                        AES_key_generate = get_random_bytes(32) # Generating the AES key which is in 128bits (i6bytes to bit)

                        rsa_cipher = PKCS1_OAEP.new(recipient_key) 
                        enc_AES_key = rsa_cipher.encrypt(AES_key_generate) # Using the recipient public key to encrypt the Aes Key

                        compress_file = 'compress_' + os.path.basename(new_path)
                        original_message = open(compress_file, 'rb')
                        textFile = original_message.read() # Reading the Plaintext File
                        textFile = bytearray(textFile) # Converting the content of the file to bit

                        aes_cipher = AES.new(AES_key_generate, AES.MODE_EAX)
                        ciphertext, tag = aes_cipher.encrypt_and_digest(textFile) # Encrypting thr file and generating the Cipher text and the hash digest(hash function)
                        encrypted_path_object = open(os.path.join(self.dir_path,encrypted_path_text), 'wb') # opening the file just created 
                        [ encrypted_path_object.write(x) for x in (enc_AES_key, aes_cipher.nonce, tag, ciphertext) ] # Storing our result in a file
                        with open(hashh, 'w') as h:
                            h.write(file_hash.hexdigest())  
                        encrypted_path_object.close()
                        original_message.close()
                        cprint('Encryption Done. Check the Directory you input for your Plain Cipher Text', color='green', attrs=['bold','blink'])                           
        return 
        
