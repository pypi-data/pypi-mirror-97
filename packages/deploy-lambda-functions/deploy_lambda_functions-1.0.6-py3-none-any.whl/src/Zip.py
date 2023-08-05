import os, shutil

class Zip:
    def __init__(self,name,path):
        self.path = self.__compress(name,path)

    def get_bytes(self):
        with open(self.path, 'rb') as file:
            return file.read()

    def __compress(self,name,path):
        print("Compressing code dir: {}".format(path))
        format = "zip"
        self.name = "{}.{}".format(name,format)
        return shutil.make_archive(name, format, path)
        
