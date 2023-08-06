#!/usr/bin/env python3

import binascii

# b'hello world' -> 'hello world'
def bytes_to_string(convert_me: bytes) -> str:
    return convert_me.decode("utf-8")

# 'hello world' -> b'hello world'
def string_to_bytes(convert_me: str) -> bytes:
    return convert_me.encode("utf-8")

# b'010203' -> b'\x01\x02\x03'
def hexstring_to_binary(convert_me: bytes) -> bytes:
    return binascii.unhexlify(hexstring)

# b'\x01\x02\x03' -> b'010203'
def binary_to_hexstring(convert_me: bytes) -> bytes:
    return binascii.hexlify(binary)

def bytes_to_bytearray(my_bytes):
    return list(my_bytes)

def bytearray_to_bytes(list_of_bytes):
    return bytes(list_of_bytes)




