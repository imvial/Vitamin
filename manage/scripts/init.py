from iscript import IScript
import sys
import shutil
import os
from vitamin.siteinfo import SiteInfo
from vitamin.config import default

class init(IScript):

    def run(self):
        self.create_simple_site()   
    
    simple_site = [
        "models",
        "templates",
        "views",
        "logic",
        "stuff/scripts",
        "stuff/styles",
        "stuff/files"]
    
    def create_simple_site(self):
        
        """
        Создает файловую структуру и все необходимые файлы
        для создания простого vitamin- сайта.
        """
        
        list(map(os.makedirs, self.simple_site)) 
        
        info = SiteInfo(
            name=input("Enter site name:"),
            description=input("Enter site description:"),
            version=input("Enter site version:"),
            authors=input("Enter site authors:"))

        info.write_to(self.currentdir)
        self.copy_config()
        
    def copy_config(self):
        try:
            default_config_file = default.__file__
            shutil.copyfile(default_config_file,
                os.path.join(self.currentdir, "config.py"))
            print("Config file [OK]")
        except:
            print("Error while creating 'config.py'")
            sys.exit(1)
        
