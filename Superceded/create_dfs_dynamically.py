import pandas
import xlsxwriter

df = pandas.read_excel(
    "/Users/carstenjuliansavage/PycharmProjects/Random_Project/Telco_customer_churn.xlsx"
)

var_list = list(df.columns)

# create an empty dictionary to store the data frames
var_dict = {}

writer = pandas.ExcelWriter('DictionaryMadeWithCarsten.xlsx', engine='xlsxwriter')

# loop over each variable name
for variable_name in var_list:
    # create an empty list to store the data frames for this variable
    variable_dfs = []
    # loop over the current column
    for col in df.columns:
        if col == variable_name:
            # create a data frame with the value counts and percentages
            var = pandas.concat([df[col].value_counts(dropna=False), df[col].value_counts(normalize=True, dropna=False)], axis=1, keys=('Count','Perc'))
            # add the data frame to the list for this variable
            variable_dfs.append(var)
    # concatenate all the data frames for this variable into one data frame
    variable_df = pandas.concat(variable_dfs, axis=0, keys=df.columns)
    # add the data frame to the dictionary with the variable name as the key
    var_dict[variable_name] = variable_df
    # write the data frame to an Excel file with the variable name as the sheet name
    variable_df.to_excel(writer, sheet_name=variable_name, index=True, header=True, freeze_panes=(1, 0))


writer.close()