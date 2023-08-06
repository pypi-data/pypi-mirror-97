from PIL import Image
import re
import os
import time
import subprocess
import logging
import platform


class CreateEBook:
    def __init__(self):
        self.data = None
        self.base_cmd = ""
        self.setup()

    def setup(self):
        if platform.system().lower() == "windows":
            self.base_cmd = '"C:\Program Files\Calibre2\ebook-convert.exe"'
            return True
        if platform.system().lower() == "linux":
            self.base_cmd = '"ebook-convert"'
            return True
        if platform.system().lower() == "darwin":
            self.base_cmd = '"ebook-convert"'
            return True

    def create_ebook(self, name, pdf_path, ebook_path):
        if os.path.exists(pdf_path):
            logging.error(pdf_path + " does not exist")
            return False, ""
        if os.path.exists(ebook_path):
            logging.error(ebook_path + " does not exist")
            return False, ""
        data = re.sub(r'[\\/*?:"<>|!]', "", name)
        data = data[data.find("]")+1:]
        name = data[:data.find("[")].strip()
        logging.info("Generating Books", pdf_path)
        ebook = self.base_cmd + ' "' + pdf_path + '" ' + '"' + "".join(ebook_path.split(".")[:-1].strip())+name + '.mobi"'
        subprocess.call(ebook, shell=True)
        return True, ebook_path
