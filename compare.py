import argparse
import os
from pathlib import Path
from bin import *

# ===== Helper functions =====
def validate_file(file_path):
    """Validates that the file exists, is a file, and is readable."""
    try:
        path = Path(file_path).resolve(strict=True)
        if not path.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        if not path.is_file():
            raise ValueError(f"'{file_path}' is not a file.")
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"File '{file_path}' is not readable.")
    except Exception as e:
        raise e


# ===== Main function with argument parsing =====

def main():
    parser = argparse.ArgumentParser(
        description="Compare two files using different methods.",
        epilog="Examples:\n"
            "  python compare.py file1.txt file2.txt --method line\n"
            "  python compare.py file1.csv file2.csv --method csv\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('file1', help="Path to the first file")
    parser.add_argument('file2', help="Path to the second file")
    parser.add_argument(
        '--method', choices=['line', 'hash', 'byte', 'csv'], default='line',
        help="Comparison method: 'line' for line-by-line, 'hash' for hash-based, 'byte' for byte-by-byte, 'csv' for csv-by-csv. Default is 'line'."
    )
    args = parser.parse_args()

    # Improved error handling for file existence and permissions
    try:
        validate_file(args.file1)
        validate_file(args.file2)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Choose comparison method
    try:
        if args.method == 'line':
            compare_files_line_by_line(args.file1, args.file2)
        elif args.method == 'hash':
            compare_files_by_hash(args.file1, args.file2)
        elif args.method == 'byte':
            compare_files_byte_by_byte(args.file1, args.file2)
        elif args.method == 'csv':
            compare_csv_cells(args.file1, args.file2)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
