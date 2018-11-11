"""
Caesar Cipher.
 
https://en.wikipedia.org/wiki/Caesar_cipher
 
"""
 
import string
import pytest
 
# Number operations.
 
def encode_number(n, shift=0):
    return (n + shift) % 26
 
def decode_number(n, shift=0):
    return (n - shift) % 26
 
# Letter operations.
 
def letter_from_number(n):
    return string.ascii_uppercase[n]
 
def number_from_letter(l):
    return string.ascii_uppercase.find(l)
 
def encode_letter(l, shift=0):
    return letter_from_number(
                encode_number(
                    number_from_letter(l), shift))
 
def decode_letter(l, shift=0):
    return letter_from_number(
               decode_number(
                   number_from_letter(l), shift))
 
# Message operations.
 
def encode_message(m, shift=0):
    return ''.join(map(lambda l: encode_letter(l, shift), m))
 
def decode_message(m, shift=0):
    return ''.join(map(lambda l: decode_letter(l, shift), m))
 
 
@pytest.mark.parametrize('cipher_shift', list(range(100)))
def test_caesar_cipher(cipher_shift):
 
    message = 'KATIE'
 
    encoded = encode_message(message, shift=cipher_shift)
    # assert encoded == 'NDWLH'
    print("encoded == {}".format(encoded))
 
    decoded = decode_message(encoded, shift=cipher_shift)
    assert decoded == message
 
 
if __name__ == '__main__':
 
    test_caesar_cipher(3)
 