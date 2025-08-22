import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(full_path).startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(os.path.abspath(full_path)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path, "r") as f:
            file_content = f.read()
        if len(file_content) > MAX_CHARS:
            file_content = (
                file_content[:MAX_CHARS]
                + f'[...File "{file_path}" truncated at 10000 characters]'
            )
        return file_content
    except Exception as e:
        return "Error: " + str(e)
