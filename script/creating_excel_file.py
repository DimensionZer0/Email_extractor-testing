import re
import pandas as pd

def making_excel(data_str,file_name,clm1,clm2):
    #pattern = r'^\d+\.'
    pattern = r'^\d+\.\s'

    if("**" not in data_str):
        column_names = ["Account Name", "First Name", "Last Name", "Gender", "Email id", "Mobile number",
                        "Billing type",
                        "Pickup Location", "Drop Location", "Booking Type",
                                                            "Booking date", "Booking time", "Booking End date",
                        "Car Type",
                        "Continuous Booking", "Disposal", "Flight Number", "Journey Type", "Special Instructions",
                        "All The dates", "Number of days cab is required"]

        lines = data_str.strip().split('\n')
        values=[]
        for i in range(0, len(lines), 1):

            #column_names.append(lines[i].split(':')[0].strip())
            values.append(lines[i].split(':', 1)[-1].strip())  ##
        # Create a dictionary from the lists
        data = {column: [value] for column, value in zip(column_names, values)}
        # Determine the maximum length among all lists
        max_len = max(len(v) for v in data.values())

        # Fill missing values with 'Not mentioned'
        for key in data:
            data[key] += ['Kinldy Check in Text Format'] * (max_len - len(data[key]))

        df = pd.DataFrame(data)
        df = df.replace(to_replace={col: {pattern: ''} for col in df.columns}, regex=True)
    else:
        column_names = (
        "Account Name", "First Name", "Last Name", "Gender", "Email id", "Mobile number", "Billing type",
        "Pickup Location", "Drop Location", "Booking Type",
                                            "Booking date", "Booking time", "Booking End date", "Car Type",
        "Continuous Booking", "Disposal", "Flight Number", "Journey Type", "Special Instructions",
        "All The dates", "Number of days cab is required")

        lines = data_str.strip().split('\n')
        clm=[]
        v=[]

        for i in range(0, len(lines), 1):
            if (("**" not in lines[i]) and lines[i] != ""):
                clm.append(lines[i].split(':')[0].strip())
                v.append(lines[i].split(':', 1)[-1].strip())  ##
        data = {column: [] for column, in zip(clm)}

        # Populate the dictionary with values
        for column, val in zip(clm, v):
            data[column].append(val)

        data = dict(zip(column_names, data.values()))
        max_len = max(len(v) for v in data.values())

        # Fill missing values with 'Not mentioned'
        for key in data:
            data[key] += ['Kinldy Check in Text Format'] * (max_len - len(data[key]))

        df = pd.DataFrame(data)
        df = df.replace(to_replace={col: {pattern: ''} for col in df.columns}, regex=True)

    df["file_name"]=clm1
    try:
        df1=pd.read_excel(file_name)
        result_df = pd.concat([df1, df], ignore_index=True)
        result_df.to_excel(file_name,index=False)
    except:
        df.to_excel(file_name,index=False)



