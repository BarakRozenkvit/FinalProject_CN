import os

class FileHandler:
    """
    This class create an instance for each file
    that responsible to split the file to chunk of data
    """
    def __init__(self,path):
        self.path = path
        if path != "" :
            self.reader = open(path,"r")
            self.file_size = os.path.getsize(self.path)
        self.eof = False

    def get_data(self,size):
        """
        check if file reader has got to the end of the file,
        if not, return the size parameter of data
        if data is less than wanted size, set self.EOF to True
        else yes set self.EOF to True
        :return:
        """
        if not self.reader.tell() == self.file_size:
            data = self.reader.read(size)
            if len(data) < size:
                self.eof = True
            
            return data
        
        else:
            self.eof = True

    def get_sequence_number(self):
        """
        get the first next byte of the package to send
        :return:
        """
        return self.reader.tell() + 1

if __name__ == '__main__':
    d = FileHandler("Files/2.txt")
    g =d.get_data(88800)
    g = d.get_data(880)