import hashlib
import argparse
import binascii

header_str = (
    "52434b530012000000a06c3780084230006bdf605334ac3ecbf993cb0c5642ef"
    "007cd2f82c39dd0000035c84392e372e312e302e313700000000000000010009"
    "0000000000000000000000000000000000000000000000000000000000000000"
    "7a6637393432000000000000392e372e312e302e313700000000000000000003"
    "8008000000000000000000000000000000000000000000000000000000000000"
)

header_template = binascii.unhexlify(header_str)

def internet_checksum(data: bytes, initial_checksum: int = 0) -> int:
    checksum = initial_checksum
    length = len(data)
    i = 0

    while i < length - 1:
        word = (data[i] << 8) + data[i + 1] 
        checksum += word
        i += 2

    if length % 2 == 1:
        checksum += data[i] << 8

    while (checksum >> 16) > 0:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return ~(checksum & 0xFFFF) & 0xFFFF


def parse_args():
    parser = argparse.ArgumentParser(description="Create uploadable OpenWrt firmware image for Ruckus ZF7363")
    parser.add_argument("file", help="OpenWrt Sysupgrade image file")

    return parser.parse_args()



"""
Header format:
- Offset `0x18`, 16 bytes: MD5 checksum of firmware (everything after header)
- Offset `0x2A`, 2 bytes (here: `0x5C84`): "Internet Checksum" (RFC 1071) of whole header (starting at `0x00`, `0x0A` bytes), except these two bytes set to zero
"""


def main():
    args = parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    header = bytearray(header_template)

    # Calculate MD5 checksum of firmware
    md5 = hashlib.md5()
    md5.update(data)
    md5_checksum = md5.digest()
    header[0x18:0x28] = md5_checksum

    # Calculate checksum of header
    header[0x2A] = 0
    header[0x2B] = 0
    header_checksum = internet_checksum(header)
    header[0x2A] = header_checksum >> 8
    header[0x2B] = header_checksum & 0xFF

    with open("factory.bin", "wb") as f:
        f.write(header)
        f.write(data)


if __name__ == "__main__":
    main()    


