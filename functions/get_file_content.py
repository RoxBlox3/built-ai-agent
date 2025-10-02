import os

from config import MAX_CHARS
from google.genai import types


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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Reads and returns the content of a specified file within the working directory. Files larger than 10000 characters will be truncated",
            ),
        },
        required=["file_path"],
    ),
)
