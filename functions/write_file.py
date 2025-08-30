import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the provided content to the specified file, constrained to the working directory. Creates directories as needed and overwrites the file if it exists.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file."
                )
            },
        ),
    )

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        path = os.path.abspath(os.path.join(working_directory, file_path))
        dirpath = os.path.dirname(path)
        if os.path.commonpath([abs_working_dir, path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        
        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
        
        
    except Exception as e:
        return f"Error: {e}"