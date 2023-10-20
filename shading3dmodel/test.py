import os
from PIL import  Image
import cv2
import tempfile
import pandas as pd
import numpy as np
from fpdf import FPDF
import unicodedata


class PDF(FPDF):
    def chapter_body(self, image_path):
        # Image dimensions
        img_width = 120
        img_height = 120

        # Calculate x, y to center the image
        x_centered = (210 - img_width) / 2  # 210 mm is the width of an A4 page
        y_centered = (297 - img_height) / 2  # 297 mm is the height of an A4 page

        self.image(image_path, x=x_centered, y=y_centered, w=img_width, h=img_height)
        self.set_font("Arial", size=12)
        self.ln(10)


def read_three_component(directory):
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            images.append(os.path.join(root, file))
    return images

# def create_pdf(image_paths):
def create_pdf(image_paths, output_pdf_path):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=25)
    
    for image_path in image_paths:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        original_image = cv2.resize(image, (800, 800))
        
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        #get inverted image
        inv_gray = 255 - gray
        # make inverted image as blur
        blurred = cv2.GaussianBlur(inv_gray, (21,21), 0,0)
        
        # get again inverted from the blur image
        inv_blurred = 255 - blurred
        
        # get the sketch of the image
        sketch = cv2.divide(gray, inv_blurred, scale=256.0)
        
        temp_dir = tempfile.mkdtemp()
        sketch_file_path = os.path.join(temp_dir, "temp_sketch.png")
        
        # Save the image
        cv2.imwrite(sketch_file_path,sketch)
        
        # add image in pdf
        pdf.add_page()
        pdf.chapter_body(sketch_file_path)
        
        cv2.waitKey()
        cv2.destroyAllWindows
    pdf.output(output_pdf_path)
    return output_pdf_path 
