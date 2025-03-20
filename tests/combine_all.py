import os


def combine_files(directories, output_file, extensions=(".py", ".qss")):
    total_lines = 0
    all_code = ""

    for directory in directories:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.endswith(extensions):
                    file_path = os.path.join(directory, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                        all_code += f"\n# File: {file}\n" + "".join(lines)

    # Save combined content to a new file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_code)

    print(f"{output_file} created with {total_lines} total lines.")


def main():
    # Define root directory
    root_dir = os.getcwd()  # Change this to your project path
    views_dir = os.path.join(root_dir, "views")
    widgets_dir = os.path.join(root_dir, "widgets")
    utils_dir = os.path.join(root_dir, "utils")
    output_file = r"tests\combined\all_combined.py"

    # Combine all files with the specified extensions into one
    directories_to_combine = []
    directories_to_combine.append(root_dir)
    directories_to_combine.append(views_dir)
    directories_to_combine.append(widgets_dir)
    # directories_to_combine.append(utils_dir)

    extensions_to_include = (".py", ".qss")

    combine_files(directories_to_combine, output_file,
                  extensions=extensions_to_include)


if __name__ == '__main__':
    main()
