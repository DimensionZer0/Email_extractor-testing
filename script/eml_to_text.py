
from email import policy
from email.parser import BytesParser
import os
import email
import base64
import html2text
import re

def eml_to_html_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        eml_content = file.read()
    msg = email.message_from_string(eml_content)
    #print(msg)

    # Check if the message is multipart
    if msg.is_multipart():

        for part in msg.walk():
            content_type = part.get_content_type()
            content_transfer_encoding = part.get('Content-Transfer-Encoding')

            if content_type == 'text/html' and content_transfer_encoding == 'base64':
                # Decode the base64 content
                encoded_content = part.get_payload()
                decoded_content = base64.b64decode(encoded_content).decode('utf-8')
                html_file_name = file_path.replace(".eml", ".html")
                with open(html_file_name, "wt") as out_file:
                    out_file.write(decoded_content)
                return html_file_name

    else:

        # If the message is not multipart, directly extract the content
        content_type = msg.get_content_type()

        content_transfer_encoding = msg.get('Content-Transfer-Encoding')

        if content_type == 'text/html' and (content_transfer_encoding == 'base64' or content_transfer_encoding=="quoted-printable"):

            # Decode the base64 content
            encoded_content = msg.get_payload()

            try:
                decoded_content = base64.b64decode(encoded_content).decode('utf-8')
            except:
                decoded_content=encoded_content
                pass

            html_file_name = file_path.replace(".eml", ".html")
            with open(html_file_name, "wt") as out_file:
                out_file.write(decoded_content)
            return html_file_name

def convert_html_to_text(html_content):
    # Create an HTML to text converter
    h = html2text.HTML2Text()

    # Convert HTML to plain text
    text_content = h.handle(html_content)

    return text_content


def read_eml_files(directory_path, output_directory):
    for filename in os.listdir(directory_path):
        if filename.endswith(".eml"):
            file_path = os.path.join(directory_path, filename)

            try:
                with open(file_path, 'rb') as file:
                    # Parse the EML file
                    msg = BytesParser(policy=policy.default).parse(file)
                    #plain_text_content = extract_plain_text(msg)

                    plain_text_content = extract_plain_text(msg,file_path)

                    # Save plain text content to a text file with the same name
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.txt")
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(plain_text_content)

                    #print(f"Processed: {file_path}. Saved as: {output_file_path}")

            except Exception as e:
                pass
                #print(f"Error processing {file_path}: {e}")

def extract_plain_text(msg,file_path):

    plain_text_content=""

    for part in msg.walk():

        if part.get_content_type() == 'text/plain':

            plain_text_content += part.get_payload()

            try:
                plain_text_content1 = base64.b64decode(plain_text_content).decode('utf-8')
                return plain_text_content1
            except:
                return plain_text_content
        if part.get_content_type()=="text/html":

            html_file_name=eml_to_html_message(file_path)


            data = ""
            with open(html_file_name, "rt") as in_file:
                for line in in_file:
                    if re.compile(r'[a-zA-Z0-9\._]+@[a-zA-Z\.]'):
                        data=data+line

                plain_text_content=convert_html_to_text(data)
            return plain_text_content



