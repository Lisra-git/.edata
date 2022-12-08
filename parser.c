#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Struct to store information about a file in the archive
typedef struct {
    char filename[128];
    int size[4];
    char hash[64];
} FileInfo;

// Struct to store information about the .edata archive
typedef struct {
    int archive_size;
    int num_files;
    FileInfo* files;
} ArchiveInfo;

// Function to parse a .edata file and extract its information
ArchiveInfo parse_edata(FILE* file) {
    ArchiveInfo info;

    // Read the archive size from the first 4 bytes of the file
    fread(&info.archive_size, sizeof(int), 1, file);

    // Read the number of files from the next 4 bytes of the file
    fread(&info.num_files, sizeof(int), 1, file);

    // Allocate memory for the FileInfo structs for each file
    info.files = malloc(info.num_files * sizeof(FileInfo));

	// Read the pointer jungle from 0x10
	fseek(file, 0x10, SEEK_SET);
    // Read the file headers from the next 10 * 4 bytes of the file
    // (10 pointers to file headers, each 4 bytes long)
    int file_headers[16];
    fread(file_headers, sizeof(int), 16, file);

    // Read the individual file headers and store the information in the FileInfo structs
    for (int i = 0; i < info.num_files; i++) {
        // Seek to the start of the file header
        fseek(file, file_headers[i], SEEK_SET);

        // Read the filename
        fread(info.files[i].filename, 1, 128, file);

        // Read the file size
        fread(&info.files[i].size, sizeof(int), 4, file);

        // Read the file hash
        fread(info.files[i].hash, 1, 64, file);
    }

    return info;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <edata file>\n", argv[0]);
        return 1;
    }

    // Open the .edata file
    FILE* file = fopen(argv[1], "r");
    if (!file) {
        printf("Error: Could not open file %s\n", argv[1]);
        return 1;
    }

    // Parse the .edata file
    ArchiveInfo info = parse_edata(file);

    // Print the information extracted from the file
    printf("Archive size: %d\n", info.archive_size);
    printf("Number of files: %d\n", info.num_files);
    printf("Files:\n");
    for (int i = 0; i < info.num_files; i++) {
        printf("  Name: %s\n", info.files[i].filename);
        printf("  Size: %d\n", info.files[i].size);
        printf("  Hash: %s\n\n", info.files[i].hash);
    }

}