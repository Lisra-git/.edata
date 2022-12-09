# .edata
Some kind of archive storing raw files primary for Numworks Epsilon apps

## File Header (archive description)

| Offset | Size | Description                                 |
|--------|------|---------------------------------------------|
| 0x00   | 0x04 | Archive size                                |
| 0x04   | 0x04 | Number of files in archive (max 16)         |
| 0x10   | 0x40 | PointerJungle: 16 x 0x4 pointers to file headers in the archive |

## File Header (For each stored file in archive)

| Offset | Size | Description                                 |
|--------|------|---------------------------------------------|
| 0x00   | 0x80 | Filename (128 characters)                   |
| 0x80   | 0x04 | Size of file in bytes                       |
| 0x84   | 0x40 | Hash of file content                        |
| 0xC4   | 0x0C | Reserved (not used for storing data)         |
| 0xD0   | -    | File content (size specified in the size of file field) |

## Builder

A python script named `build.py` is provided to build an archive. To use the script, place it in a folder, along with a new folder named `/topack/` containing the files you want to include in the archive. Then, simply run the `build.py` script.

## Parser

Two parser samples are provided, one written in C and the other in Python. These samples can be tested by passing the data file as an argument. Simply pass the path to the data file as an argument to the parser to parse the data.
