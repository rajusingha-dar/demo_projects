import os
import pathlib

# Define the project structure as a list of directories
# Using os.path.join to ensure cross-platform compatibility
directories = [
    os.path.join("app", "static", "css"),
    os.path.join("app", "static", "js"),
    os.path.join("app", "templates"),
]

# Define the list of empty files to be created
files = [
    "requirements.txt",
    ".gitignore",
    "README.md",
    os.path.join("app", "__init__.py"),
    os.path.join("app", "main.py"),
    os.path.join("app", "crud.py"),
    os.path.join("app", "models.py"),
    os.path.join("app", "schemas.py"),
    os.path.join("app", "database.py"),
    os.path.join("app", "templates", "index.html"),
    os.path.join("app", "static", "css", "styles.css"),
    os.path.join("app", "static", "js", "script.js"),
]

def create_project_structure():
    """
    Creates the directory and file structure for the project.
    """
    print("Creating project structure...")

    # Create directories
    for dir_path in directories:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"  Created directory: {dir_path}")
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")

    # Create empty files
    for file_path in files:
        try:
            pathlib.Path(file_path).touch()
            print(f"  Created file: {file_path}")
        except IOError as e:
            print(f"Error creating file {file_path}: {e}")

    print("\nProject structure created successfully!")
    print("Next steps:")
    print("1. Create a virtual environment: python -m venv venv")
    print("2. Activate it: source venv/bin/activate (on Unix) or venv\\Scripts\\activate (on Windows)")
    print("3. Populate 'requirements.txt' and install dependencies: pip install -r requirements.txt")


if __name__ == "__main__":
    create_project_structure()
