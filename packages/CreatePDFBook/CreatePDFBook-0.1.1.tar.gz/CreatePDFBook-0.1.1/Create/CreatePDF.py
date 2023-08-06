from PIL import Image
import re
import os
import time
import logging


class CreatePDF:
    def __init__(self):
        self.sorting_alg = None
        self.image_width = 1

    def create_pdf(self, name, image_loc, pdf_loc=""):
        if os.path.exists(image_loc):
            logging.error(image_loc + " does not exist")
            return False, ""
        if os.path.exists(pdf_loc):
            logging.error(pdf_loc + " does not exist")
            return False, ""
        data = re.sub(r'[\\/*?:"<>|!]', "", name)
        data = data[data.find("]") + 1:]
        name = data[:data.find("[")].strip()
        images = os.listdir(image_loc)
        images = [x for x in images if re.search("(png$)|(jpg$)|(jpeg$)", x)]
        if len(images) == 0:
            logging.warning(image_loc + " no images(png,jpg,jpeg) exist in this path")
            return False, ""
        book = []
        logging.info("Adding Pages to PDF")
        for i in images:
            current_page = image_loc + "/" + i
            book.append(self.get_image(current_page))
        pdf_name = pdf_loc + "/" + name.split(".")[0] + ".pdf"
        book[0].save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=book[1:])
        logging.info("Finished creating PDF:" + pdf_name)
        return True, pdf_name

    def get_image(self, image_dir):
        width = self.image_width
        im = Image.open(image_dir)
        left = im.size[0] * (1 - (1.0 * width))
        top = 0
        right = im.size[0] * (1.0 * width)
        bottom = im.size[1]
        im1 = im.crop((left, top, right, bottom))
        new_im = im1.convert('RGB')
        return new_im
