import os

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    dir_contents = os.listdir(path)
    result = f"Result for {"current" if directory == "." else directory} directory:"
    if not os.path.isdir(path):
        return f'{result}\n   Error: "{directory}" is not a directory'
    if not os.path.abspath(directory).startswith("/home/moonman/workspace/github.com/python-ai-agent"):
        return f'{result}\n   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    for file in dir_contents:
        cur_file_path = os.path.join(path, file)
        if os.path.isfile(cur_file_path) or os.path.isdir(cur_file_path):
            result = f"{result}\n  - {file}: file-size={os.path.getsize(cur_file_path)} bytes, is_dir={os.path.isdir(cur_file_path)}"
    return result
