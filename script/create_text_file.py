
def text_file_crate(file_path: object, content: object) -> object:
    try:
        # Try to open the file in exclusive creation mode ('x')
        with open(file_path, 'x') as file:
            # Write content to the file
            file.write(content)

    except FileExistsError:
        with open(file_path, 'a') as file:
            # Write content to the file
            file.write(content)
