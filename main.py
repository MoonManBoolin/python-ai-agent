import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    print(sys.argv)
    if (len(sys.argv) > 0):
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
        if (sys.argv[2] == "--verbose"):
            print(response.text)
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            print(response.text)
        
    else:
        print("ERROR")
        return 1


if __name__ == "__main__":
    main()
