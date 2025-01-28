import os

# Define the root directory where your project is located
root_dir = os.getcwd()  # Change this to the actual path

# List of Python files to count lines from
python_files = []

# Traverse the directory and collect Python files
for root, _, files in os.walk(root_dir):
    if "/tests" in root.replace("\\", "/"):  # Ensure cross-platform compatibility
        continue  # Skip files in the /tests directory
    
    for file in files:
        if file.endswith(".py") and not file.startswith("all_code_combined"):
            python_files.append(os.path.join(root, file))

# Count lines and copy content
total_lines = 0
all_code = ""

for file in python_files:
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        total_lines += len(lines)
        all_code += f"\n# File: {file}\n" + "".join(lines)

# Print the total line count
print(f"Total number of lines: {total_lines}")

# Save all code to a single file (optional)
#with open(r"tests\\all_code_combined.py", "w", encoding="utf-8") as f:
#    f.write(all_code)
#
#print("All code copied to 'all_code_combined.py'.")
