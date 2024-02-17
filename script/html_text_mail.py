import html2text
import re
import os


def convert_html_to_text(html_content):
    # Create an HTML to text converter
    h = html2text.HTML2Text()

    # Convert HTML to plain text
    text_content = h.handle(html_content)

    return text_content

def mail_text_file(directory_path: object, output_path: object) -> object:

    for filename in os.listdir(directory_path):
        data=""
        if filename.endswith(".html"):  # Assuming you are looking for text files, adjust as needed
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "rt") as in_file:
                for line in in_file:
                    if re.compile(r'[a-zA-Z0-9\._]+@[a-zA-Z\.]'):
                        data=data+line
                text_content = convert_html_to_text(data)

                filename=filename.replace("html","txt")
                with open(output_path+filename, "wt") as out_file:
                    out_file.write(text_content)
