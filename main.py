import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    
    is_verbose = False
    if (sys.argv[-1] == "--verbose"):
        is_verbose = True
    if (len(sys.argv) > 1):
        for f in range(20):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        tools=[available_functions]
                        ),
                    )
                
                for i in response.candidates:
                    messages.append(i.content)
                    
                if response.function_calls != None and len(response.function_calls) > 0:
                    function_responses = []
                    for function_call_part in response.function_calls:
                        print(f" - Calling function: {function_call_part.name}")
                        print(function_call_part.name)
                        function_call_result = call_function(function_call_part, is_verbose)
                        if not function_call_result.parts or not function_call_result.parts[0].function_response:
                            raise Exception("empty function call result")
                        function_responses.append(function_call_result.parts[0])
                        if is_verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                    if not function_responses:
                        raise Exception("no function responses generated, exiting.")
                    messages.append(types.Content(role="user", parts=function_responses))
                    continue
                if response.text:
                    print(response.text)
                    if is_verbose:
                        print(f"User prompt: {user_prompt}")
                        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                    break
            except Exception as e:
                print(f"Error: {e}")
                return
        
    else:
        print("ERROR")
        return 1


if __name__ == "__main__":
    main()
