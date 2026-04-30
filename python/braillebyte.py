# Constants from: https://www.unicode.org/charts/PDF/U2800.pdf
BASE_ADDRESS = 0x2800
BLOCK_OFFSET = 1 << 6
BLOCKS = 4

MAX_ADDRESS = (BASE_ADDRESS + (BLOCK_OFFSET * BLOCKS)) - 1


# Single Byte Functions
def encode_braille_byte(data: int):
    if data < 0 or data > 255:
        raise ValueError(f"Input is out of range for uint8 (0 - 255): {data}")

    sub_address_a = (data & 0b01110000) >> 4
    sub_address_b = data & 0b00000111
    sub_address = (sub_address_a << 3) | sub_address_b

    block_a = (data & 0b10000000) >> 7
    block_b = (data & 0b00001000) >> 3
    block = (block_a << 1) | block_b

    address = BASE_ADDRESS + (BLOCK_OFFSET * block) + sub_address

    return chr(address)


def is_braille_byte(data: str | int):
    if type(data) is str:
        address = ord(data)
    else:
        address = data
    
    if address < BASE_ADDRESS or address > MAX_ADDRESS:
        return False
    else:
        return True


def decode_braille_byte(data: str):
    address = ord(data)

    if not is_braille_byte(address):
        raise ValueError(f"Input is not a valid Unicode braille character (0x{BASE_ADDRESS:x} - 0x{MAX_ADDRESS:x}): \"{data}\" (Code point 0x{address:x})")
    
    address -= BASE_ADDRESS

    block_a = (address & 0b10000000) >> 7
    block_b = (address & 0b01000000) >> 6

    sub_address_a = (address & 0b00111000) >> 3
    sub_address_b = address & 0b00000111

    return (block_a << 7) | (sub_address_a << 4) | (block_b << 3) | sub_address_b


# Multi-Byte Functions
def encode_braille(data: bytearray):
    braille = ""
    for byte in data:
        braille += encode_braille_byte(byte)
    
    return braille


def is_braille(data: str):
    if len(data) == 0:
        return False
    
    for x in data:
        if not is_braille_byte(x):
            return False
    return True


def decode_braille(data: str):
    values = bytearray()
    
    for char in data:
        values.append(decode_braille_byte(char))
    
    return values
    