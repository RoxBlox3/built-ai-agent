from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python
from functions.write_file_content import write_file_content
from google.genai import types


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    functions_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python": run_python,
        "write_file_content": write_file_content,
    }

    function_name = function_call_part.name
    func = functions_map.get(function_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"
    result = func(**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
