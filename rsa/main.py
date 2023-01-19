"""Coursework for 667V0033 1CWK50
Student name: Paul Ogunniyi
Student ID: 22482234
This application was developed using code samples from:
20% Lecturer provided enc.py
40% https://pycryptodome.readthedocs.io/en/latest/src/examples.html
10% https://github.com/srimani-programmer/AES-Cryptographic-Tool
30% Paul Ogunniyi

All comments are original
"""
import sys
from termcolor import cprint, colored
from file_encryption import File_Encryption
from folder_encryption import Folder_Encryption
from decryption import Decryption
from generate_rsa import Generate_RSA
import time


space_count = 30 * ' '
print(colored('{} File Encryption And Decryption Tool. {}'.format(space_count,space_count), 'red'))
cprint('{} {}'.format(space_count + 3 * ' ','Programmed by Paul ogunniyi.'),'green')
while True:
    cprint('1. Genrate RSA key',color='magenta')
    cprint('2. Encryption',color='magenta')
    cprint('3. Decryption', color='magenta')
    cprint('4. Exit', color='red')
    cprint('~Python3:',end=' ', color='green')
    choice = int(input())

    if choice == 1:
        rsa = Generate_RSA()
        rsa.generate_rsa()
    if choice == 2:
        logo = '''  ___                       _   _          
 | __|_ _  __ _ _ _  _ _ __| |_(_)___ _ _  
 | _|| ' \/ _| '_| || | '_ \  _| / _ \ ' \ 
 |___|_||_\__|_|  \_, | .__/\__|_\___/_||_|
                  |__/|_|                  '''
        cprint(logo, color='red', attrs=['bold'])
        encfil = File_Encryption()
        encfol = Folder_Encryption()
        cprint('What do you want to encrypt', color='magenta')
        cprint('1.Single File',color='magenta')
        cprint('2. Folder', color='magenta')
        cprint('3. Exit', color='red')
        cprint('~Python3:',end=' ', color='green')
        option = int(input())
        if option == 1:
            encfil.file_encryption()
            time.sleep(2)
        elif option == 2:
            encfol.folder_encryption()
            time.sleep(2)
        elif option == 3:
            sys.exit()
        else:
            print('Choice not available')

    elif choice == 3:
        logo = '''  ___                       _   _          
 |   \ ___ __ _ _ _  _ _ __| |_(_)___ _ _  
 | |) / -_) _| '_| || | '_ \  _| / _ \ ' \ 
 |___/\___\__|_|  \_, | .__/\__|_\___/_||_|
                  |__/|_|                  '''
        cprint(logo, color='red', attrs=['bold'])
        dec = Decryption()
        cprint('What do you want to decrypt', color='magenta')        
        cprint('1.Single File',color='magenta')
        cprint('2. Folder', color='magenta')
        cprint('3. Exit', color='red')
        cprint('~Python3:',end=' ', color='green')
        option = int(input())
        if option == 1:
            dec.File_decryption()
        elif option == 2:
            dec.Folder_decryption()
        elif option == 3:
            sys.exit()
        else:
            cprint('Choice not available', color="red")
    elif choice == 4:
        sys.exit()
    else:
        cprint(' wrong choice', color="red")
