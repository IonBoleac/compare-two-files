

# Byte-by-byte comparison
def compare_files_byte_by_byte(file1, file2, chunk_size=4096):
    """Compares two files byte by byte, reading in chunks for efficiency."""
    try:
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
    except Exception as e:
        print(f"Error during byte-by-byte comparison: {e}")