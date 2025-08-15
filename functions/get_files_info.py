import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        if not os.path.abspath(full_path).startswith(
            os.path.abspath(working_directory)
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(os.path.abspath(full_path)):
            return f'Error: "{directory}" is not a directory'
        string = []
        for file in os.listdir(full_path):
            is_dir = os.path.isdir(os.path.join(full_path, file))

            string.append(
                f"- {file}: file_size={os.path.getsize(os.path.join(full_path, file))} bytes, is_dir={is_dir}"
            )
        return "\n".join(string)
    except Exception as e:
        return "Error: " + str(e)
