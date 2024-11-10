import os

class FileHandler:

    def __init__(self,path):
        """
        self.path: file path
        self.reader: file reader
        self.packageSize: package size that is random between 1000 and 2000
        self.fileSize: file size
        self.EOF: if we reach EOF
        """
        self.path = path
        if path != "" :
            self.reader = open(path,"r")
            self.file_size = os.path.getsize(self.path)
            print(self.path , " : " , self.file_size)
        self.eof = False

    def get_data(self,size):
        """
        cheבk if file reader has got to the end of the file,
        if not, return the size paramter of data
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