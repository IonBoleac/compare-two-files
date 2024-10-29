import argparse
import difflib
import hashlib
import csv

# ===== Functions for different comparison methods =====
import difflib

def compare_files_line_by_line(file1, file2):
    """Compares two files line by line and prints the differences."""
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


def compare_files_by_hash(file1, file2):
    """Compares two files by generating their SHA256 hashes."""
    def hash_file(file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    file1_hash = hash_file(file1)
    file2_hash = hash_file(file2)

    if file1_hash == file2_hash:
        print(f"Files {file1} and {file2} are identical.")
    else:
        print(f"Files {file1} and {file2} are different.")

def compare_files_byte_by_byte(file1, file2, chunk_size=4096):
    """Compares two files byte by byte, reading in chunks for efficiency."""
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while True:
            chunk1 = f1.read(chunk_size)
            chunk2 = f2.read(chunk_size)

            if chunk1 != chunk2:
                # Find the exact position where the files differ within the chunk
                for i, (b1, b2) in enumerate(zip(chunk1, chunk2)):
                    if b1 != b2:
                        position = f1.tell() - len(chunk1) + i
                        print(f"Files differ at byte position {position}")
                        return

            if not chunk1:  # End of file
                break

    print("Files are identical.")



def compare_csv_cells(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        for row_num, (row1, row2) in enumerate(zip(reader1, reader2), start=1):
            for col_num, (cell1, cell2) in enumerate(zip(row1, row2), start=1):
                if cell1.strip() != cell2.strip():  # Strip to remove any extra whitespace
                    print(f"Difference at Row {row_num}, Column {col_num}: '{cell1}' != '{cell2}'")
    print("CSV files compared and are identical.")


# ===== Main function with argument parsing =====

def main():
    parser = argparse.ArgumentParser(description="Compare two files using different methods.")
    parser.add_argument('file1', help="Path to the first file")
    parser.add_argument('file2', help="Path to the second file")
    parser.add_argument(
        '--method', choices=['line', 'hash', 'byte', 'csv'], default='line',
        help="Comparison method: 'line' for line-by-line, 'hash' for hash-based, 'byte' for byte-by-byte, 'csv' for csv-by-csv. Default is 'line'."
    )
    args = parser.parse_args()

    if args.method == 'line':
        compare_files_line_by_line(args.file1, args.file2)
    elif args.method == 'hash':
        compare_files_by_hash(args.file1, args.file2)
    elif args.method == 'byte':
        compare_files_byte_by_byte(args.file1, args.file2)
    elif args.method == 'csv':
        compare_csv_cells(args.file1, args.file2)

if __name__ == '__main__':
    main()
