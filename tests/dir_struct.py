import os
import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print the directory structure in a tree format.')
    parser.add_argument('directory', nargs='?', default=os.getcwd(), help='Directory to list (default: current directory)')
    # Default exclude list: __pycache__, .git, build, and dist
    parser.add_argument('--exclude', nargs='*', default=["__pycache__", ".git", "build", "dist", "tests"],
                        help='Directory names to exclude (default: "__pycache__ .git build dist")')
    args = parser.parse_args()

    print(f"Directory structure for: {args.directory}\n")
    print_directory_structure(args.directory, exclude=args.exclude)