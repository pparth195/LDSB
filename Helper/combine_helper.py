import pandas as pd 
import numpy as np
import openpyxl


################### For hydro oil ###################

def get_hydro_df(files):
    df = pd.DataFrame()
    for i in range(len(files)):
        data = pd.read_excel(files[i], header=9, skipfooter=3)
        data['Name'] = files[i]
        df = df.append(data)
    
    return df


def combine_hydro(df):

	df = get_hydro_df(f)

	# IN 3
	SiteName = pd.read_excel('Address Reference.xlsx')
	df = df.merge(SiteName[['Address', 'Site Name',
	                        'Facility Size (sq.ft.)']], how='left', on='Address')
	df = df[df['Reason Not Billed'] !=
	        'No billing as of summary billing cut off date']
	df = df.reset_index()
	df['Index'] = range(1, len(df)+1)

	# In 4

	hydro_one = df[['Index', ' Account Number', 'Service Classification', 'Address', 'Site Name', 'Reading From Date', 'Reading To Date',
                'Read Type', 'Metered Usage [kWh]', 'Adjusted Usage [kWh]', 'Demand [kW]', 'Total Current\nCharges ', 'Facility Size (sq.ft.)']]

	hydro_one.rename(columns={'Reading From Date': 'Start Date', 'Reading To Date': 'End Date',
	                          'Total Current\nCharges ': 'Total Amount'}, inplace=True)

	hydro_one['Utility'] = 'ELECTRIC'
	hydro_one['Provider'] = 'Hydro One'
	hydro_one['Date'] = hydro_one['Start Date']

	hydro_one['Start Date'] = pd.to_datetime(hydro_one['Start Date'])
	hydro_one['End Date'] = pd.to_datetime(hydro_one['End Date'])
	hydro_one['Date'] = pd.to_datetime(hydro_one['Date'])

	hydro_one.loc[(hydro_one['Adjusted Usage [kWh]'] == 0) | (
	    hydro_one['Adjusted Usage [kWh]'].isnull()), 'Total Consumption'] = hydro_one['Metered Usage [kWh]']

	hydro_one['Total Consumption'].fillna(
	    hydro_one['Adjusted Usage [kWh]'], inplace=True)

	# IN 5

	hydro_one['Check'] = hydro_one['Address']+hydro_one['Utility'] + \
    hydro_one['Start Date'].dt.strftime(
        '%Y-%m-%d')+hydro_one['End Date'].dt.strftime('%Y-%m-%d')
	hydro_one["Remove_Duplicates"] = hydro_one['Check']+hydro_one['Total Amount'].astype(
	    str)+hydro_one['Total Consumption'].astype(str)+hydro_one['Demand [kW]'].astype(str)

	# IN 6

	Dates = hydro_one.select_dtypes('datetime64[ns]').columns.values.tolist()
	for i in Dates:
	    hydro_one[i] = hydro_one[i].dt.date

	hydro_one['eKWh'] = hydro_one['Total Consumption']
	hydro_one.loc[((hydro_one['eKWh'] > 0) & (hydro_one['Facility Size (sq.ft.)'] > 0)),
	              'ekWh/sqft'] = hydro_one['eKWh']/hydro_one['Facility Size (sq.ft.)']

	colnames = ['Index', 'Utility', 'Provider', 'Date', 'Address', 'Site Name', 'Start Date', 'End Date',
	            'Total Amount', 'Total Consumption', 'Demand [kW]', 'Facility Size (sq.ft.)', 'eKWh', 'Facility Size (sq.ft.)']
	Final_Hydro = hydro_one.drop_duplicates(subset=['Remove_Duplicates'])
	Final_Hydro = Final_Hydro[colnames]

	return Final_Hydro

def add_single_utility_to_database(df):
	pass

