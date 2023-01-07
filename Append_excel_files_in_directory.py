# Importing packages
import pandas
import os
import glob
import openpyxl
import pickle
import numpy as np

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
    combined_files = pandas.concat([combined_files, df], ignore_index=True)


# Get first 20 rows from each source doc, shuffle obs. to increase probability of obs. in the sample.
combined_files_slim = (combined_files
                       .sample(frac=1, random_state=47)
                       .groupby(['File_Name'])
                        .head(20)
                        .set_index(['File_Name'])
                       )

# Get column names for files where data exists for those columns
NonNARows = (combined_files_slim.stack()
             .reset_index(level=1)
             .groupby(level=0,sort=False)
             ['level_1'].apply(list)
             )

NonNARows = pandas.DataFrame(NonNARows)

NonNARows['level_1']=list(map(set,NonNARows['level_1']))

