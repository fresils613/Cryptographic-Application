import zlib, sys
from termcolor import cprint
import os
# just texting

class Compress:
    def compress(self, filename):
        self.filename_in = filename # The name of the file you wish to encrypt
        new_file_name = os.path.basename(self.filename_in) # if the file name is a path, choose the last name of the path.
        self.filename_out = 'compress_' + new_file_name # where to save the compress data
        with open(self.filename_in, mode="rb") as fin: 
            data = fin.read() # Read the content of the file you wan to compress
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION) # Perform the compression

            print('---------------------------+---------------------------------------------------')
            cprint(f"Original size: {sys.getsizeof(data)}", color='blue', attrs=['bold','blink']) # get the size of the original file 
            # Original size: 1000033
            cprint(f"Compressed size: {sys.getsizeof(compressed_data)}", color='blue', attrs=['bold','blink']) # Get the size of the compressed
            # Compressed size: 1024
            print('---------------------------+---------------------------------------------------')
            fout = open(os.path.join(self.filename_out), mode="wb")
            fout.write(compressed_data)
    def decompress(self, file_compress):
        self.file_compress = file_compress 
        main = 'decompress_' + self.file_compress
        with open(self.file_compress, mode="rb") as fin, open(main, mode="wb") as fout:
            data = fin.read()
            decompressed_data = zlib.decompress(data)
            cprint(f"Compressed size: {sys.getsizeof(data)}", color='blue', attrs=['bold','blink'])
            # Compressed size: 1024
            cprint(f"Decompressed size: {sys.getsizeof(decompressed_data)}", color='blue', attrs=['bold','blink'])
            fout.write(decompressed_data)
            # Decompressed size: 10000
