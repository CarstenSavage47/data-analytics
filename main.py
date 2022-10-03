
import pandas
import openpyxl
Telco = pandas.read_excel('/Users/carstenjuliansavage/Desktop/Telco_customer_churn.xlsx')

(Telco
 .filter(['Churn Reason','City','Count','Tenure Months','Total Charges'])
 .rename(columns={'Churn Reason':"Churn_Reason",'Tenure Months':"Tenure_Months"})
 .dropna()
 .query("Churn_Reason.str.lower().str.contains('better')",engine="python")
 .query("Churn_Reason.str.lower().str.startswith('')", engine="python")
 .query("Churn_Reason.str.lower().str.endswith('r')", engine="python")
 .query("Churn_Reason.str.lower().str.contains('better|Competitor')", engine="python") # 'Or' operator
 # .query("Churn_Reason.str.lower().str.contains('better&Competitor')", engine="python") # Note, the & operator does not work.
 .query('City not in ["Columbus"]')
 .query('City in ["Los Angeles","San Francisco"]')
 .groupby('City')
 .agg({'Count':"sum",'Tenure_Months':"mean",'Total Charges':"sum",'City':pandas.Series.nunique})
 )

(Telco
 .agg({'City': pandas.Series.nunique})
 )

California = (Telco
              .query("State.str.contains('California')", engine="python")
              .sort_values('City',ascending=True)
              #.query('Contract.isna()')
              .query('Contract.notnull()')
              .assign(Nonsensical=lambda a: (a.Count+a.Latitude)/a.Longitude)
              )

City_List = ['Walnut','Diamond Bar','Rowland Heights']

WDR = (Telco
       .query('City in @City_List')
       .dropna(subset=['Latitude','Churn Reason']) # Dropping NAs in specific columns
       )




# Pulling data from Star Wars API
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

