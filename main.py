import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=sys.argv[1],
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        elif response.function_calls:
            for function_call_part in response.function_calls:
                print(
                    f"Calling function: {function_call_part.name}({function_call_part.args})"
                )
        else:
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        # sys.exit(1)


if __name__ == "__main__":
    main()
