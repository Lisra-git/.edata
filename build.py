import os
import struct
import hashlib


def get_files_size_hash():
    files = []
    for root, dirs, filenames in os.walk("topack"):
        for f in filenames:
            with open(os.path.join(root, f), "rb") as file:
                files.append((os.path.join(f), os.path.getsize(os.path.join(root, f)), hashlib.sha256(file.read()).hexdigest()))
    return files


# open outputpack.edata
with open("outputpack.edata", "wb") as outputpack:
    # in first 0x10 put header with global pack size as FFFF to be filled later and number of input files
    outputpack.write(struct.pack("<II", 0xFFFFFFFF, len(get_files_size_hash())))
    # then we will have pointer jungle of 0x40 at next aligned address storing addresses of files inside data pack we will use offset
    # so we will write 0x40 bytes of 0x00
    outputpack.seek(0x10)
    outputpack.write(b"\x00" * 0x40)

    # now we will write files
    # first we will write file header with filename, size and hash
    # then we will write file content at next 0x10 aligned address
    # we will store file address in pointer jungle
    # we will repeat this for every file

    # we will use offset to store file address in pointer jungle
    offset = 0x50
    alt_offset = 0x50
    outputpack.seek(offset)
    # write file header at offset
    for file in get_files_size_hash():
        offset = alt_offset
        outputpack.seek(offset)
        # build header as string without struct
        # filename is 128 char long
        # size is 4 bytes long
        header = file[0].ljust(128, "\x00").encode("utf-8") + struct.pack("<I", file[1]) + file[2].encode("utf-8")
        # write header
        outputpack.write(header)
        # write file content at next aligned address
        outputpack.seek((outputpack.tell() + 0xF) & ~0xF)
        with open("topack/" + file[0], "rb") as file_to_pack:
            outputpack.write(file_to_pack.read())
        # update offset with header size + filesize
        alt_offset = outputpack.tell()
        print(offset)
        # store file address in pointer jungle
        outputpack.seek(0x10 + (get_files_size_hash().index(file) * 4))
        print(0x10 + (get_files_size_hash().index(file) * 4))
        # print filename
        print(file[0])

        outputpack.write(struct.pack("<I", offset))
    # get current file size in var
    current_size = alt_offset
    # write to 0x00
    outputpack.seek(0x00)
    # get current file size in var
    current_size = alt_offset
    # write to 0x00
    outputpack.seek(0x00)
    # write current file size
    outputpack.write(struct.pack("<I", current_size))