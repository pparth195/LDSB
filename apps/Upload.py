import streamlit as st
import numpy as np
import pandas as pd
import os
import Helper.combine_helper as ch

def app():

	st.title("Upload Data")

	st.sidebar.subheader('Details of files:')
	# Sidebar Options:
	
	file_type = st.sidebar.selectbox('File Type',('Aggregated Data', 'Single Utility')),

	Utility_list = ['Hydro One', 'Suncor Oil','Superior Propane','Union Gas','Utility Kingston']
	
	if file_type:
		# st.write()
		if file_type[0] == 'Single Utility':
			st.sidebar.selectbox('Select Utility Type', Utility_list)

############################# 	body   #######################################

	st.write("specifications: ")
	
	data_file = st.file_uploader("Upload a file with above mention specifications.", type=['.xlsx', '.xls', 'csv'])


	def upload_to_db(df):
		df.to_sql('record', conn, if_exists='append', index=False)


	def transforme_utility(df):
		pass



	# Read file as df
	if data_file is not None:
		if '.csv' in data_file.name:
			df = pd.read_csv(data_file)
		else:
			# df = pd.read_excel(data_file)
			df = ch.get_hydro_df(data_file.name)

		st.write(df.head())



	def save_file(file_to_save):
		with open(os.path.join("tempDir",file_to_save.name),"wb") as f:
			f.write(file_to_save.getbuffer())
		return st.success("Saved File:{} to tempDir".format(file_to_save.name))

















	def seperate_by(sep_by):
		sites = list(df[sep_by].unique())
		# sites = list(df["Site Name"].unique())
		utility = list(df["Utility"].unique())

		for s in sites:
		    writer = pd.ExcelWriter("Seperated by school/" + s + ".xlsx")
		    for u in utility:
		        if u in ["WATER", "SEWER"]:
		            temp = df.loc[(df["Site Name"] == s) & (df["Utility"] == u), ["Utility","Start Date", "End Date", "Total Consumption"]]
		        else:
		            temp = df.loc[(df["Site Name"] == s) & (df["Utility"] == u), ["Utility","Start Date", "End Date", "eKWh"]] 
		        if temp.shape[0] > 0:
		            temp.to_excel(writer, sheet_name = u)
		    writer.save()

	# st.write(os.path)

	