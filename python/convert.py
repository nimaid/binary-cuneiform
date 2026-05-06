#!/usr/bin/env python3

import argparse
from pathlib import Path

from braillebyte import encode_braille, decode_braille, is_braille


BLOCK_SIZE = 4096


def convert_encode(input: Path, output: Path | None = None, big_endian: bool = True, block_size: int = BLOCK_SIZE):
    if output is None:
        print("\"", end="")
    else:
        fo = open(output, "w", encoding="utf-8")
    
    with open(input, "rb") as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if not block:
                break

            block_braille = encode_braille(bytearray(block), big_endian=big_endian)
            
            if output is None:
                print(block_braille, end="")
            else:
                fo.write(block_braille)
        
        if output is None:
            print("\"")
        else:
            fo.close()


def convert_decode(input: Path | str, output: Path, big_endian: bool = True, block_size: int = BLOCK_SIZE):
    if is_braille(input):
        file_input = False
        position = 0
        length = len(input)
    else:
        file_input = True
        f = open(Path(input), "r", encoding="utf-8")
    
    with open(output, "wb")  as fo:
        while True:
            if file_input:
                block = f.read(block_size)
                if not block:
                    break
            else:
                if position == length:
                    break
                    
                end_position = position + block_size
                if end_position > length:
                    end_position = length
                    
                block = input[position:end_position]
                position = end_position
            
            block_bytes = decode_braille(block, big_endian=big_endian)
            fo.write(block_bytes)
    
    if file_input:
        f.close()


def main():
    parser = argparse.ArgumentParser(description="Converts between binary files and braille.")
    
    parser.add_argument("-e", "--encode", type=Path, help="encode a binary file to braille text")
    parser.add_argument("-d", "--decode", type=str, help="decode braille text to a binary file")
    parser.add_argument("-o", "--output", type=Path, help="where to save the decoded file / encoded text")
    parser.add_argument("-l", "--little_endian", action='store_true', help="overrides the default big endian behavior")

    args = parser.parse_args()
    
    if args.encode is not None and args.decode is not None:
        print("Cannot encode and decode at the same time, exiting...")
        return 1
    if args.encode is not None:
        convert_encode(input=args.encode, output=args.output, big_endian=not args.little_endian)
    elif args.decode is not None:
        if args.output is None:
            print("No output file specified to decode to, exiting...")
            return 1
        
        convert_decode(input=args.decode, output=args.output, big_endian=not args.little_endian)
    else:
        print("Nothing to encode/decode, exiting...")
        return 1
    
    return 0


if __name__ == "__main__":
    main()
