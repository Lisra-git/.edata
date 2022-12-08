import sys
from typing import List

# Struct to store information about a file in the archive
class FileInfo:
    def __init__(self, filename: str, size: int, hash: str):
        self.filename = filename
        self.size = size
        self.hash = hash

# Struct to store information about the .edata archive
class ArchiveInfo:
    def __init__(self, archive_size: int, num_files: int, files: List[FileInfo]):
        self.archive_size = archive_size
        self.num_files = num_files
        self.files = files

# Function to parse a .edata file and extract its information
def parse_edata(file: str) -> ArchiveInfo:
    # Open the file in binary mode
    with open(file, "rb") as f:
        # Read the archive size from the first 4 bytes of the file
        archive_size = int.from_bytes(f.read(4), byteorder="little")

        # Read the number of files from the next 4 bytes of the file
        num_files = int.from_bytes(f.read(4), byteorder="little")

        # Read the pointer jungle from 0x10
        f.seek(0x10)

        # Read the file headers from the next 16 * 4 bytes of the file
        # (16 pointers to file headers, each 4 bytes long)
        file_headers = []
        for _ in range(16):
            file_headers.append(int.from_bytes(f.read(4), byteorder="little"))

        # Read the individual file headers and store the information in the FileInfo structs
        files = []
        for i in range(num_files):
            # Seek to the start of the file header
            f.seek(file_headers[i])

            # Read the filename
            filename = f.read(128).decode()

            # Read the file size
            size = int.from_bytes(f.read(4), byteorder="little")

            # Read the file hash
            hash = f.read(64).decode()

            # Add the FileInfo struct to the list of files
            files.append(FileInfo(filename, size, hash))

    # Return the parsed archive information
    return ArchiveInfo(archive_size, num_files, files)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python edata_parser.py <edata file>")
        exit()

    # Get the name of the .edata file from the command-line arguments
    edata_file = sys.argv[1]

    # Parse the .edata file
    info = parse_edata(edata_file)

    # Print the information extracted from the file
    print(f"Archive size: {info.archive_size}")
    print(f"Number of files: {info.num_files}")
    print("Files:")
    for file in info.files:
        print(f"  Name: {file.filename}")
        print(f"  Size: {file.size}")
        print(f"  Hash: {file.hash}\n")