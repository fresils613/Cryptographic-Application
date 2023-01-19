#Generating rsa key
from Crypto.PublicKey import RSA
import os
from termcolor import cprint
import getpass 

class Generate_RSA:
    def generate_rsa(self):
        cprint('Enter the Directory Path you wish to save your public key (use / instead of \):',end=' ', color='blue', attrs=['bold','blink'])
        self.pub_dir_path = input()
        cprint('Enter the Directory Path you wish to save your private key (use / instead of \):',end=' ', color='blue', attrs=['bold','blink'])
        self.pri_dir_path = input() # store the user input inside the variable dir_path 
        key = RSA.generate(2048) # generate the key and specify the key size
        os.makedirs(self.pub_dir_path, exist_ok=True) # Create the directory specify by the user above.
        os.makedirs(self.pri_dir_path, exist_ok=True) 

        
        passphrase = getpass.getpass("Enter a passphrase to encrypt the private key: ") # ask the used for passpharase to protect the private key.
        private_key = key.export_key(passphrase=passphrase) # Use to generate the private key using the passphrase as extra security
        file_out = open(os.path.join(self.pri_dir_path,"private.pem"), "wb") # create the file for the private key result
        file_out.write(private_key) # store the private key in the file created. 
        file_out.close() # close the file 
        private_key_file = os.path.join(self.pri_dir_path,"private.pem")
        os.system("attrib +H " + private_key_file) # Used to hide the file private.pem


        public_key = key.publickey().export_key() # generate the public key from the key specify above (Can be public knowledge so there is no need for extra security)
        file_out = open(os.path.join(self.pub_dir_path,"public.pem"), "wb") # Create the file for the public key
        file_out.write(public_key) # store the result of the public key in the file created/\.
        file_out.close() # close the file


