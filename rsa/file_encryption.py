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

# Class Declaration
class File_Encryption:
    def random(self, filename, hashh, file_hash): # create a fuction that accept filename, hashh and file_hash as parameter
        self.filename = filename # store the filename parameter inside a new file called self.filename
        new_file_name = os.path.basename(self.filename) # if the fllename specify is a path, pick the last value of the file, if its a value, use the value
        try:
            cprint('Enter the Directory Path you wish to save your encrypted Files(use / instead of \):',end=' ', color='blue', attrs=['bold','blink'])
            self.dir_path = input() # using the sanitize function above, store the user input inside dir_path
        except (IOError, FileNotFoundError): # Enter if there is any error with the filename/directory name
            cprint('There is a problem with the {self.dir_path} path.'.format(self.filename), color='red',attrs=['bold','blink']) # It is used to give the error color red.
            sys.exit(0) # Terminate the code
        
        
        c = Compress() # create an instance of class Compress(Compress class is in another file called zip.py)
        c.compress(self.filename) # send the filename to a function in the compress class as parameter resul: A new file is created called (compress+_filename)
        cprint('Compression Done. Time for encryption ', color='green', attrs=['bold','blink'])

        # Opening the file
        compress_file = 'compress_' + new_file_name 
        original_message = open(compress_file, 'rb') # opened the newly created compressed file.
        
        os.makedirs(self.dir_path, exist_ok=True)	
        new_file_name = os.path.basename(self.filename)
        encrypted_file_text = 'cipher_' + new_file_name #Add cipher to the name of the file (Used to save the cipher text)
        encrypted_file_object = open(os.path.join(self.dir_path,encrypted_file_text),'wb') # opening the file just created and save the result in the folder the user input 
        content = original_message.read() # Reading the Plaintext File
        content = bytearray(content) # Converting the content of the file to bit

        AES_key = get_random_bytes(32) # Generating the AES key which is in 256bits (16bytes to bit)
        cipher_aes = AES.new(AES_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(content) # Encrypting the file and generating the Cipher text and the hash digest(hash function)

        cprint('Input the public key file or directory (use / instead of \): ',end=' ', color='red', attrs=['bold','blink'])
        receiver = input()
        recipient_key = RSA.import_key(open(receiver).read()) # Public Key of the receiver 
        cipher_rsa = PKCS1_OAEP.new(recipient_key) 
        enc_AES_key = cipher_rsa.encrypt(AES_key) # Using the recipient public key to encrypt the Aes Key 

        # encrypted_security_object.write(enc_AES_key) # Storing our cipher text in a file           
        [encrypted_file_object.write(x) for x in (enc_AES_key,cipher_aes.nonce, tag, ciphertext)]
        with open(hashh, 'w') as h: # open the file represented by variable hashh
            h.write(file_hash.hexdigest()) # store the value of hash inside the file opened above.

        encrypted_file_object.close() # close the file
        original_message.close()      # close the file
        # os.remove(compress_file)      # Remove the file from the system
        cprint('Encryption Done. Check the Directory you input for your Cipher Text', color='green', attrs=['bold','blink'])  
        return 
    def file_encryption(self):
        try:
            cprint('Enter the file name or Path: ',end=' ', color='blue', attrs=['bold','blink'])
            self.filename = input()
        except (IOError, FileNotFoundError): # Enter if there is any error with the filename/directory name
            cprint('File with name {self.filename} is not found.'.format(self.filename), color='red',attrs=['bold','blink']) # It is used to give the error color red.
            sys.exit(0) # Terminate the code
        hashh = 'Hash_' + os.path.basename(self.filename)
        with open(self.filename,'rb') as f: # Open the file to read it's bytes
            file_hash = sha256() # Create the hash object using sha256 
            fb = f.read() # Read the content of the file.
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read() # Read the next block from the file
        if os.path.isfile(hashh): # Enter, if the file specify by the variable hashh exist
            with open(hashh, 'r') as h: 
                previous_hash = h.read() # Read the content of the hash and store it in a variable called previous_hash
                if previous_hash == file_hash.hexdigest(): #  comparing the two hash. 
                    cprint('Already hashed, No new modification', color='red', attrs=['bold','blink'])
                else:
                    enc = File_Encryption() 
                    enc.random(self.filename, hashh, file_hash) # Accessing the function created above and passing filename, hashh and filename as parameter
        else: # Enter, if the file specify by the variable hashh does not exist
            enc = File_Encryption() 
            enc.random(self.filename, hashh, file_hash) # Accessing the function created above and passing filename, hashh and filename as parameter

