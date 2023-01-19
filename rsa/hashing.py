from  hashlib import sha256
from msilib.schema import Directory
import os

class Hashing:
    def __init__(self, filename):
        self.filename = filename
        # self.dir_path = directory 
        self.BLOCK_SIZE = 65538
    def hashing(self):
        file_hash = sha256() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(self.filename,'r',encoding='utf-8', errors='ignore') as f: # Open the file to read it's bytes
            fb = f.read() # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb.encode('utf-8')) # Update the hash
                fb = f.read() # Read the next block from the file
        # os.makedirs(self.dir_path, exist_ok=True)
        new_file_name = os.path.basename(self.filename)
        hash_file = "Hash_" + new_file_name
        hash_file_object = open(hash_file, 'w')
        hash_file_object.write(file_hash.hexdigest())
        hash_file_object.close()