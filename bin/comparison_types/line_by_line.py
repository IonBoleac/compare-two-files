import difflib


# Line-by-line comparison
def compare_files_line_by_line(file1, file2):
    """Compares two files line by line and prints the differences."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

        # Generate a unified diff and print if differences exist
        diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=file1, tofile=file2)
        differences = list(diff)
        
        if differences:
            print("Differences found:")
            for line in differences:
                print(line, end='')
        else:
            print("Files are identical.")
            
        # Check if one file has extra lines
        if len(file1_lines) != len(file2_lines):
            print(f"\nFiles differ in length: {file1} has {len(file1_lines)} lines, {file2} has {len(file2_lines)} lines.")
    except Exception as e:
        print(f"Error during line-by-line comparison: {e}")

