import os

from google.genai import types


def write_file_content(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
    except Exception as e:
        return "Error: " + str(e)
    try:
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return "Error: " + str(e)


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Writes content to a specified file, constrained to the working directory. Creates directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file where content should be written, relative to the working directory. Directories will be created as needed.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
