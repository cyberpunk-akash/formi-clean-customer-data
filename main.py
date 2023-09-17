import json
import pandas as pd
import os
from openpyxl import Workbook
import boto3
import io


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    if event:
        print("Hey this is event")
        s3_records = event["Records"][0]
        bucket_name = str(s3_records["s3"]["bucket"]["name"])
        file_name = str(s3_records["s3"]["object"]["key"])
        file_obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_content = file_obj["Body"].read()

        read_excel_data = io.BytesIO(file_content)
        organizer_name = os.path.splitext(file_name)[0]
        print(organizer_name)
        # original_df = pd.read_excel(read_excel_data)
        sheet_names = pd.ExcelFile(read_excel_data).sheet_names
        print(str(sheet_names))
        clean_data_dict = {}

        for sheet_name in sheet_names:
            df = pd.read_excel(read_excel_data, sheet_name)
            df_new = df.fillna(value=0)

            rows = len(df.index)
            columns = len(df.columns)

            row_no = -1
            col_no = -1
            final_number = -1
            flag = 0
            for row in range(5):
                if flag == 1:
                    break
                for col in range(columns):
                    value = df.iloc[row, col]

                    if (isNumber(df.iloc[row, col])):
                        row_no = row
                        col_no = col
                        flag = 1
                        break
                    else:
                        continue

            count_zero = 0
            i = 0

            for value in df_new[df_new.columns[col_no]]:

                if (value == 0):
                    if (count_zero == 3):
                        break
                    count_zero += 1

                else:
                    valid_number = getValidNumber(value)
                    if (isNumber(valid_number)):
                        print(valid_number)
                        if (clean_data_dict.get(valid_number) == None):
                            if isValidName(str(df_new.iloc[i, col_no - 1])) == True:
                                name = str(df_new.iloc[i, col_no - 1])
                            else:
                                name = ""
                            clean_data_list = []
                            clean_data_list.append(name)
                            clean_data_list.append(sheet_name)
                            clean_data_dict[valid_number] = clean_data_list
                        else:
                            clean_data_dict[valid_number][1] += ", " + sheet_name

                i += 1

        file_name = "CustomerData.xlsx"
        sheet_name = "CustomerData"

        workbook = Workbook()
        workbook['Sheet'].title = sheet_name
        sheet = workbook.active
        sheet['A1'].value = "Customer Name"
        sheet['B1'].value = "Phone Number"
        sheet['C1'].value = "Client ID"
        sheet['D1'].value = "Tags"

        i = 2

        for customer_entry in clean_data_dict:
            print(clean_data_dict[customer_entry][0] + "\t" + str(customer_entry)
                  + "\t" + organizer_name + "\t" + clean_data_dict[customer_entry][1])
            sheet.cell(row=i, column=1).value = clean_data_dict[customer_entry][0]
            sheet.cell(row=i, column=2).value = str(customer_entry)
            sheet.cell(row=i, column=3).value = organizer_name
            sheet.cell(row=i, column=4).value = clean_data_dict[customer_entry][1]
            i += 1

        # workbook.save(file_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def isValidName(name):
    name = str(name).replace(" ", "")
    if len(name) >= 0 and (name[0] >= 'A' and name[0] <= 'Z') or (name[0] >= 'a' and name[0] <= 'z'):
        return True
    else:
        return False


def isNumber(cell_data):
    try:
        cell_data = str(cell_data).replace(" ", "")

        if cell_data[0:3] == '+91':
            number = int(float(cell_data[3:]))
            number = str(number)
            if len(number) == 10:
                return True
            else:
                return False

        if cell_data[0:2] == '91':
            number = int(float(cell_data[2:]))
            number = str(number)
            if len(number) == 10:
                return True
            else:
                return False

        if len(str(int(float(cell_data)))) == 10:
            return True
        else:
            return False
    except:
        print('')


def getValidNumber(number):
    try:
        valid_number = str(number).replace(" ", "")

        if valid_number[0:3] == '+91':
            valid_number = int(float(valid_number[3:]))
            valid_number = str(valid_number)
            if len(valid_number) == 10:
                return int(valid_number)
            else:
                return -1

        if valid_number[0:2] == '91':
            valid_number = int(float(valid_number[2:]))
            valid_number = str(valid_number)
            if len(valid_number) == 10:
                return int(valid_number)
            else:
                return -1

        if len(str(int(float(valid_number)))) == 10:
            return int(float(valid_number))
        else:
            return False
    except:
        print('')