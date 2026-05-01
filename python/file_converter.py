#!/usr/bin/env python3

import argparse
from pathlib import Path

from braillebyte import encode_braille, decode_braille, is_braille


BLOCK_SIZE = 4096


def main():
    parser = argparse.ArgumentParser(description="Converts between binary files and braille.")
    
    parser.add_argument("-e", "--encode", type=Path, help="encode a binary file to braille text")
    parser.add_argument("-d", "--decode", type=str, help="decode braille text to a binary file")
    parser.add_argument("-o", "--output", type=Path, help="where to save the decoded file / encoded text")
    parser.add_argument("-r", "--reverse", action='store_true', help="reverses the endianness of each byte")

    args = parser.parse_args()
    
    if args.encode is not None and args.decode is not None:
        print("Cannot encode and decode at the same time, exiting...")
        return 1
    
    if args.encode is not None:
        if args.output is None:
            print("\"", end="")
        else:
            fo = open(args.output, "w", encoding="utf-8")
        
        with open(args.encode, "rb") as f:
            while True:
                block = f.read(BLOCK_SIZE)
                if not block:
                    break

                block_braille = encode_braille(bytearray(block), endian_reverse=args.reverse)
                
                if args.output is None:
                    print(block_braille, end="")
                else:
                    fo.write(block_braille)
            
            if args.output is None:
                print("\"")
            else:
                fo.close()
    elif args.decode is not None:
        if args.output is None:
            print("No output file specified to decode to, exiting...")
            return 1
        
        if is_braille(args.decode):
            file_input = False
            position = 0
            length = len(args.decode)
        else:
            file_input = True
            f = open(Path(args.decode), "r", encoding="utf-8")
        
        with open(args.output, "wb")  as fo:
            while True:
                if file_input:
                    block = f.read(BLOCK_SIZE)
                    if not block:
                        break
                else:
                    if position == length:
                        break
                        
                    end_position = position + BLOCK_SIZE
                    if end_position > length:
                        end_position = length
                        
                    block = args.decode[position:end_position]
                    position = end_position
                
                block_bytes = decode_braille(block, endian_reverse=args.reverse)
                fo.write(block_bytes)
        
        if file_input:
            f.close()
    else:
        print("Nothing to encode/decode, exiting...")
        return 1
    
    return 0


if __name__ == "__main__":
    main()
