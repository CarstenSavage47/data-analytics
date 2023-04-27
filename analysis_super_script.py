import pandas
from pandas import ExcelWriter
import os
import glob
import string
import re
import openpyxl
import pickle
import numpy as np
from loguru import logger
from openpyxl import load_workbook


pandas.set_option("display.max_rows", None)
pandas.set_option("display.max_columns", None)
pandas.set_option("display.width", None)
pandas.set_option("display.max_colwidth", None)


directory_of_interest = (
    "/Users/carstenjuliansavage/Desktop/R Working Directory/Accounting"
)

analysis_file_name = "hello"

excel_analysis_output_path = f"{directory_of_interest}/{analysis_file_name}.xlsx"


def concat_all_data(directory):
    os.chdir(directory)

    # Import files
    path = "*"
    files = glob.glob(path)

    combined_files = pandas.DataFrame()

    logger.info("Importing Files")

    list_of_dfs = []

    for each_file in files:
        if "xlsx" in each_file:
            df = pandas.read_excel(each_file, engine="openpyxl")
            df["File_Name"] = each_file
            df["Row_Number"] = df.index + 2
            list_of_dfs.append(df)
        elif "xls" in each_file:
            df = pandas.read_excel(each_file)
            df["File_Name"] = each_file
            df["Row_Number"] = df.index + 2
            list_of_dfs.append(df)
        elif "csv" in each_file:
            df = pandas.read_csv(each_file)
            df["File_Name"] = each_file
            df["Row_Number"] = df.index + 2
            list_of_dfs.append(df)
        else:
            pass

    combined_files = pandas.concat(list_of_dfs, ignore_index=True)

    logger.info("Finished Importing Files")

    return combined_files


def create_summary_of_data(data_for_summary):
    logger.info("Building non-null summary of data")

    counts_by_file = pandas.DataFrame(data_for_summary.groupby("File_Name").count())
    counts_by_file = counts_by_file.transpose()

    counts_by_file = counts_by_file.astype("int")

    counts = pandas.DataFrame(data_for_summary.count())

    master_dtypes = pandas.DataFrame(master_dataframe.dtypes)

    counts_master_and_all = pandas.concat(
        [master_dtypes, counts, counts_by_file], axis=1
    )

    counts_master_and_all.columns.values[0] = "Master_Dataset_Dtype"

    counts_master_and_all.columns.values[1] = "Master_Dataset_Non_Null"

    counts_master_and_all.drop("File_Name", axis=0, inplace=True)

    return counts_master_and_all


def get_column_names(combined_files):
    logger.info("Creating summary of names of non-null columns")

    # Get first 20 rows from each source doc, shuffle obs. to increase probability of obs. in the sample.
    combined_files_random_sample = (
        combined_files.sample(frac=1, random_state=47)
        .groupby(["File_Name"])
        .head(20)
        .set_index(["File_Name"])
    )

    # Get column names for files where data exists for those columns
    non_na_rows = (
        combined_files_random_sample.stack()
        .reset_index(level=1)
        .groupby(level=0, sort=False)["level_1"]
        .apply(list)
    )

    non_na_rows = pandas.DataFrame(non_na_rows)

    non_na_rows["level_1"] = list(map(set, non_na_rows["level_1"]))

    #non_na_rows = non_na_rows.transpose()

    return non_na_rows


def get_frequency_table(dataset):
    list_of_dfs = []
    for column in dataset:
        column_frequency = dataset[column].value_counts()
        column_frequency_df = pandas.DataFrame(column_frequency)
        list_of_dfs.append(column_frequency_df)
    return list_of_dfs


def get_frequency_table_sheets(dataset, column_name_list):
    logger.info("Creating list of dataframes")
    all_frequency_table_sheets_list = []
    for i in range(len(dataset.columns)):
        frequency_table_sheet = pandas.concat(
            [
                dataset[dataset.columns[i]].value_counts(dropna=False),
                dataset[dataset.columns[i]].value_counts(normalize=True, dropna=False),
            ],
            axis=1,
            keys=("Count", "Perc"),
        )
        all_frequency_table_sheets_list.append(frequency_table_sheet)

    return all_frequency_table_sheets_list


def save_frequency_tables_xls(list_dfs, xls_path, list_of_column_names):
    logger.info("Creating analysis Excel file")
    with ExcelWriter(xls_path) as writer:
        non_na_rows_all.to_excel(
            writer,
            sheet_name="non_na_rows_all",
            index=True,
            header=True,
            freeze_panes=(1, 0),
        )
        summary_of_master_data.to_excel(
            writer,
            sheet_name="summary_of_master_data",
            index=True,
            header=True,
            freeze_panes=(1, 0),
        )
        for df, column_name in zip(list_dfs, list_of_column_names):
            df.to_excel(
                writer,
                sheet_name=column_name,
                index=True,
                header=True,
                freeze_panes=(1, 0),
            )

    return list_of_column_names


def get_valid_excel_column_names(list_of_col_names):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    list_of_col_names = [
        "".join(c for c in col if c in valid_chars) for col in list_of_col_names
    ]
    invalid_chars = r"[\[\]:/\\?\*]"
    list_of_col_names = [re.sub(invalid_chars, "", col) for col in list_of_col_names]
    list_of_col_names = [col[:30].strip() for col in list_of_col_names]
    return list_of_col_names


if __name__ == "__main__":
    master_dataframe = concat_all_data(directory_of_interest)
    list_of_columns_in_df = master_dataframe.columns
    non_na_rows_all = get_column_names(master_dataframe)
    summary_of_master_data = create_summary_of_data(master_dataframe)

    list_of_frequency_dfs = get_frequency_table(master_dataframe)

    column_names_list = get_valid_excel_column_names(list(master_dataframe.columns))

    list_of_all_frequency_table_sheets = get_frequency_table_sheets(
        dataset=master_dataframe, column_name_list=column_names_list
    )
    save_frequency_tables_xls(
        list_dfs=list_of_all_frequency_table_sheets,
        xls_path=excel_analysis_output_path,
        list_of_column_names=column_names_list,
    )

    logger.info("Done.")
