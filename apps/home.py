import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
import pdf2image
from datetime import datetime
import pytesseract

from helper_functions import get_data_from_txt, get_loyalist_data, get_napanee_data

# for server
# pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
# for local 
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def get_text(file):
            txt = pytesseract.image_to_string(file)
            return txt



def app():

    st.title('Extract Image')

    st.set_option('deprecation.showfileUploaderEncoding', False)

    ############## Side bar ####################################
    provider_options = ["Loyalist Township", "Greater Nepanee"]
    provider = st.sidebar.selectbox("Select Provider:", 
    provider_options)
    data_file = None
    if provider:
        #############  LOYALIST ############
        if provider == provider_options[0]:
            data_file = st.file_uploader("Upload a file with above mention specifications.", type=[".png", ".jpg"])
            temp_file = NamedTemporaryFile(delete=False)

            if data_file:

                img = data_file.read()
                st.image(img, use_column_width = True)

                temp_file.write(data_file.getvalue())

                flag = 0
                if flag == 0:
                    converted_txt = str(get_text(temp_file.name))
                    flag = 1
                # st.write(type(converted_txt))
                data = get_loyalist_data(converted_txt)

                df = pd.DataFrame(data, index=[0])
                st.dataframe(df)


        ############  NAPANEE #############
        if provider == provider_options[1]:
            # st.write("Under Development!")
            data_file = st.file_uploader("Upload a file with above mention specifications.", type=[".png", ".jpg"])
            temp_file = NamedTemporaryFile(delete=False)

            if data_file:

                img = data_file.read()
                st.image(img, use_column_width = True)

                temp_file.write(data_file.getvalue())

                flag = 0
                if flag == 0:
                    converted_txt = str(get_text(temp_file.name))
                    flag = 1
                # st.write(type(converted_txt))
                data = get_napanee_data(converted_txt)

                df = pd.DataFrame(data, index=[0])
                st.dataframe(df)
        
        
        

        # if data_file:

        #     temp_file.write(data_file.getvalue())

        #     flag = 0
        #     if flag == 0:
        #         converted_txt = str(get_text(temp_file.name))
        #         flag = 1
        #     # st.write(type(converted_txt))
        #     data = get_loyalist_data(converted_txt)

        #     df = pd.DataFrame(data, index=[0])
        #     st.dataframe(df)

        #     if data:
        #         st.text_input("From:", df["From"].values[0])
        #         st.text_input("To:", df["To"].values[0])
        #         st.text_input("Consuption:", df["consumption"].values[0])
        #         st.text_input("Amount:", df["amount"].values[0])
        #         submit = st.button("Submit")

        #         if submit:
        #             st.success("Record Saved!")





        



	






    # st.title('Home')

    # st.write("This is a sample home page in the mutliapp.")
    # st.write("See `apps/home.py` to know how to use it.")

    # st.markdown("### Sample Data")
    # df = create_table()
    # st.write(df)

    # st.write('Navigate to `Data Stats` page to visualize the data')


