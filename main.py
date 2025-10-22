import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python
from functions.write_file_content import schema_write_file_content
from call_function import call_function


def main():
    if len(sys.argv) < 2 or not sys.argv[1]:
        print(
            "No input provided. Please provide a prompt as an argument.",
            file=sys.stderr,
        )
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python,
            schema_write_file_content,
        ],
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=sys.argv[1])],
    )

    messages = [user_message]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        for candidate in response.candidates:
            messages.append(candidate.content)
            if response.text:
                print(response.text)
                break
        if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=True)
                parts = getattr(function_call_result, "parts", None)
                if not parts or not getattr(parts[0], "function_response", None):
                    raise RuntimeError("Missing function response from call_function()")

                resp = parts[0].function_response.response
                if not resp:
                    raise RuntimeError("Empty function response from call_function()")
                if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
                    print(f"-> {resp}")
        else:
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        # sys.exit(1)


if __name__ == "__main__":
    main()
