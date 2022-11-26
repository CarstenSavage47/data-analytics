# Importing packages
import pandas
import os
import glob
import openpyxl
import pickle

pandas.set_option('display.max_rows',None)
pandas.set_option('display.max_columns',None)
pandas.set_option('display.width',None)
pandas.set_option('display.max_colwidth',None)

os.chdir("/Users/carstenjuliansavage/PycharmProjects/Random_Project")

# Import Excel files
path = '*.xlsx'
files = glob.glob(path)

# Loop through
combined_files = pandas.DataFrame()

for i in files:
    df = pandas.read_excel(i)
    df['File_Name'] = i
    df['Row_Number'] = df.index+2
    combined_files = combined_files.append(df, ignore_index=True)


# Slim down to get only first row from each dataset
combined_files = (combined_files
                  .groupby('File_Name')
                  .first()
                  )


# Get column names for files where data exists for those columns
NonNARows = (combined_files.stack()
             .reset_index(level=1)
             .groupby(level=0,sort=False)
             ['level_1'].apply(list)
             )

