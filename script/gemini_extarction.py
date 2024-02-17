####main code
import json
import os

import google.generativeai as genai
import time
from script.creating_excel_file import making_excel

from script.create_text_file import text_file_crate
from script.eml_to_text import read_eml_files
import pandas as pd
# Set options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def out_split(data_str):
    if ("**" not in data_str):
        lines = data_str.strip().split('\n')

        column_names = []
        values = []

        for i in range(0, len(lines), 1):
            column_names.append(lines[i].split(':')[0].strip())
            values.append(lines[i].split(':')[-1].strip())

        # Create a dictionary from the lists
        data = {column: [value] for column, value in zip(column_names, values)}
        df = pd.DataFrame(data)

    else:
        lines = data_str.strip().split('\n')
        clm = []
        v = []

        for i in range(0, len(lines), 1):
            if (("**" not in lines[i]) and lines[i] != ""):
                clm.append(lines[i].split(':')[0].strip())
                v.append(lines[i].split(':')[-1].strip())

        data = {column: [] for column, in zip(clm)}

        # Populate the dictionary with values
        for column, val in zip(clm, v):
            data[column].append(val)
        df = pd.DataFrame(data)
    return df

def gemini_extraction(input_directory="",output_dir="",System_prompt="",User_Requirements_prompt="",Emai_prompt="",temperature=0,top_p=.90):
    if(input_directory!=""):
        output_directory=input_directory
        read_eml_files(input_directory, output_directory)
        directory_path = input_directory#"text_mail_txt"
    gemini_api_key = "AIzaSyBs80fNGbHUcKiI4oYhWp3sZZ7lfy5sWWA"
    genai.configure(api_key = gemini_api_key)
    prompt = System_prompt + "\n" + User_Requirements_prompt + " "  # Added closing parentheses

    def google_gemini_model(prompt,email_data,temperature=temperature,top_p=top_p):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{prompt} /n {email_data}",generation_config=genai.GenerationConfig(top_p=top_p,temperature=temperature))
        return response.text

    def save_data(content, text_file="", final_output_gemini=""):
        output_google = google_gemini_model(prompt, content)
        final_output_gemini = text_file + "\n" + final_output_gemini + output_google
        final_output_gemini = final_output_gemini + "\n" + "-" * 50 + "\n"
        if(output_dir!=""):
            text_file_crate(output_dir + "/booking_info_gemini.text", final_output_gemini)
            making_excel(output_google, output_dir + "/booking_info_gemini.xlsx", text_file,
                         "Gemini")
            with open(output_dir + "/booking_info_gemini.json", 'a') as json_file:
                json_file.write(json.dumps(output_google, indent=4))
                json_file.write('\n')
        return output_google

    if (len(Emai_prompt) > 0):
        content = Emai_prompt
        output=save_data(content, text_file="", final_output_gemini="")
    else:
        file_list = os.listdir(directory_path)
        text_files = [file for file in file_list if file.endswith('.txt')]
        for text_file in text_files:
            file_path = os.path.join(directory_path, text_file)
            with open(file_path, 'r') as file:
                content = file.read()
                final_output_gemini = ""
                output=save_data(content,text_file=text_file,final_output_gemini=final_output_gemini)


    if(input_directory!=""):
        return output
    else:
        return out_split(output)


    print("Process Completed & All the output are inside outcome Directory")