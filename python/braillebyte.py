# Constants from: https://www.unicode.org/charts/PDF/U2800.pdf
BASE_ADDRESS = 0x2800
MAX_ADDRESS = 0x28FF


def is_braille_byte(data: str | int):
    if type(data) is str:
        address = ord(data)
    else:
        address = data
    
    if address < BASE_ADDRESS or address > MAX_ADDRESS:
        return False
    else:
        return True


def encode_braille_byte(data: int):
    if data < 0 or data > 255:
        raise ValueError(f"Input is out of range for uint8 (0 - 255): {data}")
    
    address = (data & 0b00000001) << 7
    address |= (data & 0b00000010) << 4
    address |= (data & 0b00000100) << 2
    address |= (data & 0b00001000)
    address |= (data & 0b00010000) << 2
    address |= (data & 0b00100000) >> 3
    address |= (data & 0b01000000) >> 5
    address |= (data & 0b10000000) >> 7
    
    address += BASE_ADDRESS

    return chr(address)


def decode_braille_byte(braille: str):
    address = ord(braille)

    if not is_braille_byte(address):
        raise ValueError(f"Input is not a valid Unicode braille character (0x{BASE_ADDRESS:x} - 0x{MAX_ADDRESS:x}): \"{braille}\" (Code point 0x{address:x})")
    
    address -= BASE_ADDRESS

    data = (address & 0b10000000) >> 7
    data |= (address & 0b00100000) >> 4
    data |= (address & 0b00010000) >> 2
    data |= (address & 0b00001000)
    data |= (address & 0b01000000) >> 2
    data |= (address & 0b00000100) << 3
    data |= (address & 0b00000010) << 5
    data |= (address & 0b00000001) << 7
    
    return data


# Multi-Byte Functions
def is_braille(data: str):
    if len(data) == 0:
        return False
    
    for x in data:
        if not is_braille_byte(x):
            return False
    return True


def encode_braille(data: bytearray):
    braille = ""
    for byte in data:
        braille += encode_braille_byte(byte)
    
    return braille


def decode_braille(braille: str):
    data = bytearray()
    
    for char in braille:
        data.append(decode_braille_byte(char))
    
    return data
