import numpy as np
import pandas
import openpyxl
import datetime as dt
from datetime import datetime
from fnmatch import fnmatch
import numpy as np

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


''' Flag bonanza '''
ParkNorth = Telco.copy()
City_Names = list(['Park','North'])
searchstr = '|'.join(City_Names)
To_Flag = (ParkNorth[ParkNorth['City'].str.contains(searchstr)])
To_Flag['Flag'] = 1
ParkNorth = To_Flag.combine_first(ParkNorth)



# Easy way to get top observation for a given column
WDR[WDR['Total Charges']==WDR['Total Charges'].max()]

# Dense Rank example
WDR_DRank = WDR.copy()
WDR_DRank['Rank'] = WDR['Total Charges'].rank(method='dense',ascending=False).astype(int)
WDR_DRank = WDR_DRank.sort_values(by='Rank',ascending=True)


## Using a function to classify obs
def expensive(x):
    if x == 0: return 'N/A'
    elif x <= 200: return 'Substantial'
    elif x <= 2000: return 'Significant'
    else: return 'Big Bucks'

WDR_DRank['Expensive'] = WDR_DRank['Total Charges'].apply(expensive)


'''Function using multiple columns'''
def churn_calc(column):
    if column['Churn Score'] > 0:
        return(column['Churn Value']/column['Churn Score'])
    else: return 0

Telco['churn_calc'] = Telco.apply(churn_calc,axis=1)




# Working with Functions Across Columns:

import datetime as dt

Meta_Customer_Revenue = pandas.read_excel('/Users/carstenjuliansavage/Desktop/R Working Directory/Useful Datasets/Meta_Customer_Revenue.xlsx')

Meta_Customer_Revenue = (Meta_Customer_Revenue
                        .astype({"order_shipped":'datetime64[ns]',"order_date":'datetime64[ns]'})
                         )

Meta_Customer_Revenue.dtypes

# This function gets the difference between the order_shipped and order_date columns,
# ...standardizes that to a number of days, and then divides that by 365.25 days/year to get number of years.
def Time_Length(column):
    return ((column['order_shipped'] - column['order_date']).days)/365.25

Meta_Customer_Revenue['Date_Diff_Years'] = Meta_Customer_Revenue.apply(Time_Length, axis=1)

Meta_Customer_Revenue['Day'] = Meta_Customer_Revenue['order_date'].dt.day
Meta_Customer_Revenue['Month'] = Meta_Customer_Revenue['order_date'].dt.month
Meta_Customer_Revenue['Year'] = Meta_Customer_Revenue['order_date'].dt.year







# Create a pivot table with the index as Customer ID, we want the City var categories to be columns,
# ... and values from the Total Charges column.
Example_Pivot = WDR.pivot_table(index='CustomerID',columns='City',values='Total Charges')

# Axis = 0 -- Concat the dataframe to the end
# Same number of columns, twice the obs
Big_Concat = pandas.concat([California,California],axis=0)

# Axis = 1 -- Concat the dataframe on the side
# Twice the columns, same number of obs
Big_Concat = pandas.concat([California,California],axis=1)





# Employees and Orders

Employees = pandas.read_csv('/Users/carstenjuliansavage/PycharmProjects/Random_Project/employees.csv')
Orders = pandas.read_csv('/Users/carstenjuliansavage/PycharmProjects/Random_Project/orders.csv')

# Pandas Merge. Left_on and right_on are useful when the column names for the keys are different but the data is the same.

Employee_Orders = Employees.merge(Orders, how='inner', left_on='id', right_on='id'#, suffixes=('_Employee', '_Orders')
                                  )
'''Lag Equivalent -- Lag by 4'''
Employee_Orders['Lag'] = Employee_Orders['item_cost'].shift(4)

'''Replace all nan values with inf values'''
Employee_Orders = Employee_Orders.replace(np.nan,np.inf)
'''Replace all inf values with nan values'''
Employee_Orders = Employee_Orders.replace(np.inf,np.nan)
'''Replace string within variable/column obs.'''
Employee_Orders['item'] = Employee_Orders['item'].apply(lambda x:str(x).replace("roll","ROLL"))
