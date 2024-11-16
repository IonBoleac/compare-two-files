# Description: Compare two CSV files cell by cell.
import csv
import pandas as pd
from pathlib import Path

def compare_csv_cells_(file1, file2):
    """Compares two CSV files cell by cell."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)

            for row_num, (row1, row2) in enumerate(zip(reader1, reader2), start=1):
                for col_num, (cell1, cell2) in enumerate(zip(row1, row2), start=1):
                    if cell1.strip() != cell2.strip():  # Strip to remove any extra whitespace
                        print(f"Difference at Row {row_num}, Column {col_num}: '{cell1}' != '{cell2}'")
        print("CSV files compared.")
    except Exception as e:
        print(f"Error during CSV comparison: {e}")



def compare_csv_cells(file1, file2, delimiter=',', ignore_columns=None, equivalent_values=None, output_report=None):
    """
    Compares two CSV files cell by cell with options to ignore columns, treat values as equivalent, 
    and generate a difference report.

    Args:
        file1 (str): Path to the first CSV file.
        file2 (str): Path to the second CSV file.
        delimiter (str): Delimiter used in the CSV files. Default is ','.
        ignore_columns (list of str): List of column names to ignore during comparison.
        equivalent_values (dict): Dictionary of equivalent values, e.g., {"NA": "", "null": ""}.
        output_report (str): Path to save the difference report as a CSV file.
    """
    try:
        # Load CSV files into pandas DataFrames for easier handling
        df1 = pd.read_csv(file1, delimiter=delimiter)
        df2 = pd.read_csv(file2, delimiter=delimiter)

        # Compare headers first
        if list(df1.columns) != list(df2.columns):
            print("CSV headers differ:")
            print(f"{file1} headers: {list(df1.columns)}")
            print(f"{file2} headers: {list(df2.columns)}")
            return

        # Drop ignored columns
        if ignore_columns:
            df1.drop(columns=ignore_columns, inplace=True, errors='ignore')
            df2.drop(columns=ignore_columns, inplace=True, errors='ignore')

        # Normalize equivalent values
        if equivalent_values:
            df1.replace(equivalent_values, inplace=True)
            df2.replace(equivalent_values, inplace=True)

        # Check for structural differences (e.g., row count)
        if len(df1) != len(df2):
            print(f"CSV files differ in row count: {file1} has {len(df1)} rows, {file2} has {len(df2)} rows.")

        # Compare cell by cell
        differences = []
        for row_idx in range(max(len(df1), len(df2))):
            row1 = df1.iloc[row_idx] if row_idx < len(df1) else None
            row2 = df2.iloc[row_idx] if row_idx < len(df2) else None

            if row1 is not None and row2 is not None:
                for col_name in df1.columns:
                    val1 = row1.get(col_name, None)
                    val2 = row2.get(col_name, None)
                    if val1 != val2:
                        differences.append({
                            "Row": row_idx + 1,
                            "Column": col_name,
                            "File1_Value": val1,
                            "File2_Value": val2
                        })
            elif row1 is not None or row2 is not None:
                differences.append({
                    "Row": row_idx + 1,
                    "Column": "N/A",
                    "File1_Value": row1.to_dict() if row1 is not None else "Row Missing",
                    "File2_Value": row2.to_dict() if row2 is not None else "Row Missing"
                })

        # Print summary of differences
        if differences:
            print(f"Differences found: {len(differences)}")
            for diff in differences:
                print(f"Row {diff['Row']}, Column {diff['Column']}: '{diff['File1_Value']}' != '{diff['File2_Value']}'")
        else:
            print("CSV files are identical.")

        # Generate a report if requested
        if output_report:
            Path(output_report).parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(differences).to_csv(output_report, index=False)
            print(f"Difference report saved to: {output_report}")

    except Exception as e:
        print(f"Error during CSV comparison: {e}")

