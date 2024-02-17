import os
import email
import base64

def eml_html(directory_path,output_path):
    path = os.listdir(directory_path)
    for file_name in path:
        file_path = os.path.join(directory_path, file_name)
        # Read the EML file
        with open(file_path, 'r', encoding='utf-8') as file:
            eml_content = file.read()

        # Parse the EML content
        msg = email.message_from_string(eml_content)

        # Check if the message is multipart
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_transfer_encoding = part.get('Content-Transfer-Encoding')

                if content_type == 'text/html' and content_transfer_encoding == 'base64':
                    # Decode the base64 content
                    encoded_content = part.get_payload()
                    decoded_content = base64.b64decode(encoded_content).decode('utf-8')

                    # Fix the replacement and open the HTML file for writing
                    html_file_name = file_name.replace("eml", "html")
                    with open( output_path+ html_file_name, "wt") as out_file:
                        out_file.write(decoded_content)

        else:
            # If the message is not multipart, directly extract the content
            content_type = msg.get_content_type()
            content_transfer_encoding = msg.get('Content-Transfer-Encoding')

            if content_type == 'text/html' and content_transfer_encoding == 'base64':
                # Decode the base64 content
                encoded_content = msg.get_payload()
                decoded_content = base64.b64decode(encoded_content).decode('utf-8')

                # Fix the replacement and open the HTML file for writing
                html_file_name = file_name.replace("eml", "html")
                with open(output_path + html_file_name, "wt") as out_file:
                    out_file.write(decoded_content)

