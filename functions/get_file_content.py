import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.commonpath([abs_working_dir, path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        result = ""
        with open(os.path.join(os.path.abspath(working_directory), file_path), "r") as f:
            file_contents = f.read(MAX_CHARS)
            if len(file_contents) >= MAX_CHARS:
                result = f'{file_contents}\n[...File "{file_path}" truncated at 10000 characters]'
            else:
                result = file_contents
        return result
    except Exception as e:
        return f"Error: {e}"