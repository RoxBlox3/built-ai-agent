import os

from config.py import TOKEN_LENGTH


def get_file_content(working_directory, file_path):
    try:
        if not os.path.abspath(file_path).startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(os.path.abspath(file_path)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(os.path.abspath(file_path), "r") as f:
            file_content = f.read()
        if len(file_content) > TOKEN_LENGTH:
            file_content = (
                file_content[:TOKEN_LENGTH]
                + f'[...File "{file_path}" truncated at 10000 characters]'
            )
    except Exception as e:
        return "Error: " + str(e)
