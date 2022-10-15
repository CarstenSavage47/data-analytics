
import pandas
import openpyxl
import datetime as dt
from datetime import datetime

Telco = pandas.read_excel('/Users/carstenjuliansavage/PycharmProjects/Random_Project/Telco_customer_churn.xlsx')


## General data manipulation example
(Telco
 .filter(['Churn Reason','City','Count','Tenure Months','Total Charges'])
 .rename(columns={'Churn Reason':"Churn_Reason",'Tenure Months':"Tenure_Months"})
 .dropna()
 .query("Churn_Reason.str.lower().str.contains('better')",engine="python")
 .query("Churn_Reason.str.lower().str.startswith('c')", engine="python")
 .query("Churn_Reason.str.lower().str.endswith('r')", engine="python")
 .query("Churn_Reason.str.lower().str.contains('better|competitor')", engine="python") # 'Or' operator
 # .query("Churn_Reason.str.lower().str.contains('better&competitor')", engine="python") # Note, the & operator does not work.
 .query('City not in ["Columbus"]')
 .query('City in ["Los Angeles","San Francisco"]')
 .groupby('City')
 .agg({'Count':"sum",'Tenure_Months':"mean",'Total Charges':"sum",'City':pandas.Series.nunique})
 )


# Unique city observations

(Telco
 .agg({'City': pandas.Series.nunique})
 )


# Example of null values, assign function, sort_values, and assign (R Tidyverse mutate equivalent).

California = (Telco
              .query("State.str.contains('California')", engine="python")
              .sort_values('City',ascending=True)
              #.query('Contract.isna()')
              .query('Contract.notnull()')
              .assign(Nonsensical=lambda a: (a.Count+a.Latitude)/a.Longitude)
              )

# Creating a list to use later

City_List = ['Walnut','Diamond Bar','Rowland Heights']

# WDR = Walnut, Diamond Bar, Rowland Heights

WDR = (Telco
       .filter(['City','Latitude','Longitude','Total Charges','Churn Reason'])
       .query('City in @City_List') # Querying in a list
       .dropna(subset=['Latitude','Churn Reason']) # Dropping NAs in specific columns
       )


# Easy way to get top observation for a given column

WDR[WDR['Total Charges']==WDR['Total Charges'].max()]


# Dense Rank example

WDR_DRank = WDR.copy()
WDR_DRank['Rank'] = WDR['Total Charges'].rank(method='dense',ascending=False).astype(int)
WDR_DRank = WDR_DRank.sort_values(by='Rank',ascending=True)


# Using a function to classify obs

def EXPENSIVE(x):
    if x == 0: return 'N/A'
    elif x <= 200: return 'Substantial'
    elif x <= 2000: return 'Significant'
    else: return 'Big Bucks'

WDR_DRank['Expensive'] = WDR_DRank['Total Charges'].apply(EXPENSIVE)


# Create a pivot table with the index as Customer ID, we want the City var categories to be columns,
# ... and values from the Total Charges column.
Example_Pivot = WDR.pivot_table(index='CustomerID',columns='City',values='Total Charges')
#   City        Rowland Heights  Walnut
#   CustomerID
#   3606-TWKGI          1364.30     NaN
#   4317-VTEOA            50.75     NaN
#   4587-NUKOX              NaN  246.50
#   5906-CVLHP          2319.80     NaN
#   8722-NGNBH              NaN  223.45

# Concatenations

# Axis = 0 -- Concat the dataframe to the end
# Same number of columns, twice the obs
Big_Concat = pandas.concat([California,California],axis=0)

# Axis = 1 -- Concat the dataframe on the side
# Twice the columns, same number of obs
Big_Concat = pandas.concat([California,California],axis=1)




## Bank Investments

Bank_Investments = pandas.read_excel('/Users/carstenjuliansavage/PycharmProjects/Random_Project/Analytics_mindset_case_studies_Bank_Investment_Portfolios.xlsx')

Bank_Investments_II = Bank_Investments.copy()

#Creating month-year variable, working with datetimes, dates

Bank_Investments_II['Time_DMY'] = pandas.to_datetime(Bank_Investments_II['Date'], format = '%y-%m-%d').dt.strftime('%d-%m-%y')



# Employees and Orders

Employees = pandas.read_csv('/Users/carstenjuliansavage/PycharmProjects/Random_Project/employees.csv')
Orders = pandas.read_csv('/Users/carstenjuliansavage/PycharmProjects/Random_Project/orders.csv')

# Pandas Merge. Left_on and right_on are useful when the column names for the keys are different but the data is the same.

Employee_Orders = Employees.merge(Orders, how='inner', left_on='id', right_on='id'#, suffixes=('_Employee', '_Orders')
                                  )


# Pulling data from Star Wars API Example

import requests
import json
import ijson
from pandas.io.json import json_normalize

response = requests.get("https://swapi.dev/api/people")
response.json()
print(response.text)
response.json().keys()
response.json()['results']
People_JSON = response.json()['results']
People = pandas.json_normalize(People_JSON)

