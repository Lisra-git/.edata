# .edata
Some kind of archive storing raw files primary for Epsilon apps

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
