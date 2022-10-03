
import pandas
import openpyxl
Telco = pandas.read_excel('/Users/carstenjuliansavage/Desktop/Telco_customer_churn.xlsx')

(Telco
 .rename(columns={'Churn Reason':"Churn_Reason"})
 .dropna()
 .query("Churn_Reason.str.lower().str.contains('better')",engine="python")
 .query("Churn_Reason.str.lower().str.startswith('')", engine="python")
 .query("Churn_Reason.str.lower().str.endswith('r')", engine="python")
 .query("Churn_Reason.str.lower().str.contains('better|Competitor')", engine="python") # 'Or' operator
 # .query("Churn_Reason.str.lower().str.contains('better&Competitor')", engine="python") # Note, the & operator does not work.
 .query('City not in ["Columbus"]')
 .query('City in ["Los Angeles","San Francisco"]')

 )




