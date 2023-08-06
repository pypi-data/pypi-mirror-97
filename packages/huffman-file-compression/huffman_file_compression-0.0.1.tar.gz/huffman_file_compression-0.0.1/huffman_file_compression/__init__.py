import os 
import heapq
import pickle
import ntpath


class HuffmanCompressor():
    ''' This is the main class for the implementaion of the compression/decompression
        logic using the Huffman Encoding alogrithm
    '''
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}


    class HeapNode:
        ''' Heap class to store the root and child information on the heap object'''
        def __init__(self,char,freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
        

        def __lt__(self,other):
            return self.freq < other.freq
        

        def __eq__(self,other):
            if other == None:
                return False
            if not isinstance(other,HeapNode):
                return False
            return self.freq == other.freq
    

    def get_frequency(self,text):
        ''' fetch the data frequency of the text file'''
        frequency = {}
        for char in text:
            if not char in frequency:
                frequency[char] = 0
            frequency[char] += 1
        return frequency


    def create_heap(self,frequency):
        '''Create a priority queue using the in heap'''
        for key in frequency:
            node = self.HeapNode(key,frequency[key])
            heapq.heappush(self.heap,node)


    def merge_data(self):
        '''Build the Huffman Tree'''
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merge_val = self.HeapNode(None,node1.freq + node2.freq)
            merge_val.left = node1
            merge_val.right = node2
            heapq.heappush(self.heap,merge_val)
    

    def make_code(self,root,present_val):
        ''' Recursive function call to creat the character structure'''
        if root == None:
            return
        if root.char != None:
            self.codes[root.char] = present_val
            self.reverse_mapping[present_val] = root.char
            return        
        self.make_code(root.left,present_val+"0")
        self.make_code(root.right,present_val+"1")


    def create_code(self):
        '''Create respective codes for characters and save'''
        root = heapq.heappop(self.heap)
        present_val = ""
        self.make_code(root,present_val)
    

    def encode_data(self,text):
        encode_data = ""
        for char in text:
            encode_data += self.codes[char]
        return encode_data


    def pad_encode_data(self,encoded_data):
        '''Padding the encoded data, to keep the byte level  processing in tact(the data rendered should be a multiple of 8)'''
        padding_needed = 8 - len(encoded_data)%8
        for i in range(padding_needed):
            encoded_data += "0"        
        padded_data = "{0:08b}".format(padding_needed)
        encoded_data = padded_data + encoded_data
        return encoded_data
    
    
    def get_byte_array(self,padded_encoded_data):
        ''' Creates a binay data array for the encoded padded string'''
        if (len(padded_encoded_data) % 8 != 0):
            return False
        barray = bytearray()
        for i in range(0,len(padded_encoded_data),8):
            byte = padded_encoded_data[i:i+8]
            barray.append(int(byte,2))
        return barray


    def get_pickle_filename(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    
    def get_reverse_map(self,reverse_map):
        ''' Fetches the reverse map file from the pickled map file'''
        filename = self.get_pickle_filename(reverse_map)
        with open(f'{filename}', 'rb') as handle:
            reverse_map_dict = pickle.load(handle)
        return reverse_map_dict


    def remove_padding(self,padded_encoded_data):
        ''' Funtion to remove the padded bits to restore the original data '''
        padding_info = padded_encoded_data[:8]
        extra_padding = int(padding_info,2)
        padded_encoded_data = padded_encoded_data[8:]
        encoded_data = padded_encoded_data[:-1*extra_padding]
        return encoded_data


    def decode_data(self,encoded_data,reverse_map):
        ''' The encoded string is decoded to the original format using the frquence hash map created'''
        current_data = ""
        decode_data = ""
        for bit in encoded_data:
            current_data += bit
            if(current_data in reverse_map):
                char = reverse_map[current_data]
                decode_data += char
                current_data = ""
        return decode_data


    def compress_file(self,path):
        ''' Caller function to compress the file specified'''
        try:
            filename,file_extn = os.path.splitext(path)
            out_path = f'{filename}.bin'
            with open(path,'r') as in_file , open(out_path,'wb') as out_file :
                text = in_file.read()
                text  = text.rstrip()
                frequency = self.get_frequency(text)
                self.create_heap(frequency)
                self.merge_data()
                self.create_code()
                encode_data = self.encode_data(text)
                padded_encoded_data = self.pad_encode_data(encode_data)
                barray = self.get_byte_array(padded_encoded_data)
                out_file.write(bytes(barray))
                with open(f'{filename}.pickle','wb') as map_file:
                    pickle.dump(self.reverse_mapping, map_file, protocol=pickle.HIGHEST_PROTOCOL)
            print('file compressed')
            return out_path
        except FileNotFoundError:
            print('Incorrect file path or filename')
            raise
        except IOError:
            print('Could not read the file name provide {}'.format(path))
            raise
    

    def decompress_data(self,input_file,reverse_map=None):
        ''' Caller function to decompress the file specified'''
        try:
            if not self.reverse_mapping:
                reverse_map = self.get_reverse_map(reverse_map)
                if not reverse_map:
                    raise IOError
            else:
                reverse_map = self.reverse_mapping
            filename, fileext = os.path.splitext(input_file)
            output_file = f"{filename}_decompressed.txt"
            with open(input_file,'rb') as file , open(output_file,'w') as out_file:
                bit_string = ""
                byte = file.read(1)
                while len(byte) > 0:
                    byte = ord(byte)
                    bits = bin(byte)[2:].rjust(8,'0')
                    bit_string += bits
                    byte = file.read(1)
                encoded_data = self.remove_padding(bit_string)
                decompressed_data = self.decode_data(encoded_data,reverse_map)
                out_file.write(decompressed_data)
            print("data decompressed")
            return output_file
        except FileNotFoundError:
            print('Incorrect file path or filename')
            raise
        except IOError:
            print('Could not process the file name provide {} as the data decode hash map is unavailable'.format(input_file))
            raise