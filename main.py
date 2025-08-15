import os
import sys
from dotenv import load_dotenv
from google import genai


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

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=sys.argv[1],
        )
        if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            # print(f"response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # sys.exit(1)


if __name__ == "__main__":
    main()
