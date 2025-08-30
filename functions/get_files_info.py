import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

def get_files_info(working_directory, directory="."):
    path = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_dir = os.path.abspath(working_directory)
    dir_contents = os.listdir(path)
    result = f"Result for {"current" if directory == "." else directory} directory:"
    
    if not os.path.isdir(path):
        return f'{result}\n   Error: "{directory}" is not a directory'
    if os.path.commonpath([abs_working_dir, path]) != abs_working_dir:
        return f'{result}\n   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    for file in dir_contents:
        cur_file_path = os.path.join(path, file)
        if os.path.isfile(cur_file_path) or os.path.isdir(cur_file_path):
            result = f"{result}\n  - {file}: file-size={os.path.getsize(cur_file_path)} bytes, is_dir={os.path.isdir(cur_file_path)}"
    return result
