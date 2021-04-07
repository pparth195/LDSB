import streamlit as st
import pandas as pd
import numpy as np
# from data.create_data import create_table
from rpy2.robjects.packages import importr
from tempfile import NamedTemporaryFile
import pdf2image
from datetime import datetime

from helper_functions import get_data_from_txt

import rpy2.robjects as ro
package_name = ('tesseract')
try:
    pkg = importr(package_name)
except:
    ro.r(f'install.packages("{package_name}")')
    pkg = importr(package_name)




def app():

    st.title('About')

    st.set_option('deprecation.showfileUploaderEncoding', False)

    data_file = st.file_uploader("Upload a file with above mention specifications.", type=['.xlsx', '.xls', 'csv',".pdf", ".png", ".jpg"])
    
    temp_file = NamedTemporaryFile(delete=False)
    
    
    def get_text(file):
        # img_path = r"C:\Users\Parth\Downloads\document-page2\document-page2-1.jpg"

        txt= pkg.ocr(file)
        return txt

    if data_file:
        # data = upload.read()
        
        
        temp_file.write(data_file.getvalue())

        flag = 0
        if flag == 0:
            converted_txt = str(get_text(temp_file.name))
            flag = 1
        # st.write(type(converted_txt))
        data = get_data_from_txt(converted_txt)

        st.write(data)




        # PDF to Image
        # img = pdf2image.convert_from_bytes(data_file.read())
        # st.write(get_text(img))





        



	






    # st.title('Home')

    # st.write("This is a sample home page in the mutliapp.")
    # st.write("See `apps/home.py` to know how to use it.")

    # st.markdown("### Sample Data")
    # df = create_table()
    # st.write(df)

    # st.write('Navigate to `Data Stats` page to visualize the data')


