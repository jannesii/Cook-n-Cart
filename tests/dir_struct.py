import os

def print_directory_structure(root_dir, prefix='', exclude=None):
    if exclude is None:
        exclude = []
    files = sorted(os.listdir(root_dir), key=lambda x: (not os.path.isdir(os.path.join(root_dir, x)), x.lower()))
    count = len(files)
    for index, file in enumerate(files):
        path = os.path.join(root_dir, file)
        # Skip directories if they are in the exclusion list
        if os.path.isdir(path) and file in exclude:
            continue
        connector = "└── " if index == count - 1 else "├── "
        print(prefix + connector + file)
        if os.path.isdir(path):
            extension = "    " if index == count - 1 else "│   "
            print_directory_structure(path, prefix + extension, exclude)
            
def main():
    # Hard-coded settings
    directory_to_list = os.getcwd()  # Change this to your desired directory
    exclude_dirs = ["__pycache__", ".git", "dist", "tests", ".buildozer", "apk", ".venv", ".vscode", "apk"]

    print(f"Directory structure for: {directory_to_list}\n")
    print_directory_structure(directory_to_list, exclude=exclude_dirs)

if __name__ == '__main__':
    main()