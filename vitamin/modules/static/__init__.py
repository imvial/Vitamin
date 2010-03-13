import os
from vitamin.config import Parameter, tweak, Section

class Storage():
    
    name = ""
    files = ""
    extensions = []
    path = None
    
    def __init__(self, name, path=None, extensions=[]):
        
        assert isinstance(name, str)
        assert isinstance(name, path)
        assert extensions
        
        self.name = name
        self.path = path
        self.extensions = extensions
        
        if path and os.path.exists(path):
            
            self.files = [os.path.join(path, x) for x in os.listdir(path)
                          if os.path.splitext(x)[1] in extensions]           
            
            print("storage: files in '{0}' storage -> ".format(self.name),
                ", ".join([os.path.split(x)[1] for x in self.files]))
            
    
class StorageSystem():
    
    def __init__(self, site_config):
        
        self.FOLDERS = Parameter()
        self.FOLDER_EXTENSIONS = Parameter()        
        tweak(self, "Site", site_config)
        
        assert isinstance(self.FOLDERS, Section)
        self.FOLDERS.preload()
        
        self.storages = {}

        for name, path in self.FOLDERS.items():
            if name in self.FOLDER_EXTENSIONS:
                self.add_storage(Storage(name, path, self.FOLDER_EXTENSIONS[name]))
            else:
                raise Exception("Укажите расширения файлов для хранилища '{0}'".format(name))

    def add_storage(self, storage):
        
        assert storage
        self.storages[storage.name] = storage
        
    def del_storage(self, storage=None, name=None):
        
        assert storage.name or name in self.categories
        del self.storages[storage.name or name]
        
    def resolve(self, pretty):
        
        """
            pretty: "storage.<storage_name>.file_ext"
        """
    
