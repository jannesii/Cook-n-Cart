import os

# Define root directories
root_dir = os.getcwd() # Change this to your project path
views_dir = os.path.join(root_dir, "views")
widgets_dir = os.path.join(root_dir, "widgets")

# Function to combine files in a directory
def combine_files(directory, output_file):
    total_lines = 0
    all_code = ""

    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.endswith(".py"):
                file_path = os.path.join(directory, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    all_code += f"\n# File: {file}\n" + "".join(lines)

    # Save combined content to a new file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_code)

    print(f"{output_file} created with {total_lines} total lines.")

# Combine views and widgets separately
combine_files(views_dir, r"tests\\combined\\views_combined.py")
combine_files(widgets_dir, r"tests\\combined\\widgets_combined.py")
combine_files(root_dir, r"tests\\combined\\app_combined.py")
