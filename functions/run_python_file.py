import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the specified Python file with optional arguments, constrained to the working directory. Captures and returns both standard output and error output from the execution.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(type=types.Type.STRING),
                    description="A list of arguments to pass to the Python file. Each argument has to be a string."
                )
            },
        ),
    )

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        path = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.commonpath([abs_working_dir, path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        args_processed = ["python", file_path] + args
        completed_process_obj = subprocess.run(args_processed, timeout=30, cwd=abs_working_dir, capture_output=True)
        if not completed_process_obj.stdout and not completed_process_obj.stderr:
            return "No output produced"
            
        return f"STDOUT: \n{completed_process_obj.stdout.decode("utf-8")}\nSTDERR: \n{completed_process_obj.stderr.decode("utf-8")}\n{f"Process exited with code {completed_process_obj.returncode}" if completed_process_obj.returncode != 0 else ""}"
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    