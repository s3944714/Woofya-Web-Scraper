import os
import ast

def find_imports_in_file(file_path):
    """Find and return a list of imported libraries from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r') as file:
            node = ast.parse(file.read(), filename=file_path)
            for item in node.body:
                if isinstance(item, ast.Import):
                    for alias in item.names:
                        imports.add(alias.name)
                elif isinstance(item, ast.ImportFrom):
                    imports.add(item.module)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return imports

def find_imports_in_directory(directory):
    """Find all imported libraries in Python files within a directory."""
    all_imports = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                all_imports.update(find_imports_in_file(file_path))
    return all_imports

if __name__ == "__main__":
    project_directory = '.'  # Change this to your project path if needed
    imported_libraries = find_imports_in_directory(project_directory)
    
    print("Imported Libraries:")
    for library in sorted(imported_libraries):
        print(library)
