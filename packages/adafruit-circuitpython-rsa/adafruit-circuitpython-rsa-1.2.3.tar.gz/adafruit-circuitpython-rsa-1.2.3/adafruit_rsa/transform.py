# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
# SPDX-License-Identifier: Apache-2.0

"""Data transformation functions.

From bytes to a number, number to bytes, etc.
"""

# from __future__ import absolute_import

from struct import pack
import adafruit_binascii as binascii

from adafruit_rsa._compat import byte, is_integer
from adafruit_rsa import common, machine_size

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RSA.git"


def bytes2int(raw_bytes):
    """Converts a list of bytes or an 8-bit string to an integer.

    When using unicode strings, encode it to some encoding like UTF8 first.

    >>> (((128 * 256) + 64) * 256) + 15
    8405007
    >>> bytes2int(b'\x80@\x0f')
    8405007

    """

    return int(binascii.hexlify(raw_bytes), 16)


def _int2bytes(number, block_size=None):
    """Converts a number to a string of bytes.

    Usage::

        >>> _int2bytes(123456789)
        b'\x07[\xcd\x15'
        >>> bytes2int(_int2bytes(123456789))
        123456789

        >>> _int2bytes(123456789, 6)
        b'\x00\x00\x07[\xcd\x15'
        >>> bytes2int(_int2bytes(123456789, 128))
        123456789

        >>> _int2bytes(123456789, 3)
        Traceback (most recent call last):
        ...
        OverflowError: Needed 4 bytes for number, but block size is 3

    @param number: the number to convert
    @param block_size: the number of bytes to output. If the number encoded to
        bytes is less than this, the block will be zero-padded. When not given,
        the returned block is not padded.

    @throws OverflowError when block_size is given and the number takes up more
        bytes than fit into the block.
    """

    # Type checking
    if not is_integer(number):
        raise TypeError(
            "You must pass an integer for 'number', not %s" % number.__class__
        )

    if number < 0:
        raise ValueError("Negative numbers cannot be used: %i" % number)

    # Do some bounds checking
    if number == 0:
        needed_bytes = 1
        raw_bytes = [b"\x00"]
    else:
        needed_bytes = common.byte_size(number)
        raw_bytes = []

    # You cannot compare None > 0 in Python 3x. It will fail with a TypeError.
    if block_size and block_size > 0:
        if needed_bytes > block_size:
            raise OverflowError(
                "Needed %i bytes for number, but block size "
                "is %i" % (needed_bytes, block_size)
            )

    # Convert the number to bytes.
    while number > 0:
        raw_bytes.insert(0, byte(number & 0xFF))
        number >>= 8

    # Pad with zeroes to fill the block
    if block_size and block_size > 0:
        padding = (block_size - needed_bytes) * b"\x00"
    else:
        padding = b""

    return padding + b"".join(raw_bytes)


def bytes_leading(raw_bytes, needle=b"\x00"):
    """
    Finds the number of prefixed byte occurrences in the haystack.

    Useful when you want to deal with padding.

    :param raw_bytes:
        Raw bytes.
    :param needle:
        The byte to count. Default \x00.
    :returns:
        The number of leading needle bytes.
    """

    leading = 0
    # Indexing keeps compatibility between Python 2.x and Python 3.x
    _byte = needle[0]
    for x in raw_bytes:
        if x == _byte:
            leading += 1
        else:
            break
    return leading


def int2bytes(number, fill_size=None, chunk_size=None, overflow=False):
    """
    Convert an unsigned integer to bytes (base-256 representation)::
    Does not preserve leading zeros if you don't specify a chunk size or
    fill size.
    .. NOTE:
        You must not specify both fill_size and chunk_size. Only one
        of them is allowed.
    :param number:
        Integer value
    :param fill_size:
        If the optional fill size is given the length of the resulting
        byte string is expected to be the fill size and will be padded
        with prefix zero bytes to satisfy that length.
    :param chunk_size:
        If optional chunk size is given and greater than zero, pad the front of
        the byte string with binary zeros so that the length is a multiple of
        ``chunk_size``.
    :param overflow:
        ``False`` (default). If this is ``True``, no ``OverflowError``
        will be raised when the fill_size is shorter than the length
        of the generated byte sequence. Instead the byte sequence will
        be returned as is.
    :returns:
        Raw bytes (base-256 representation).
    :raises:
        ``OverflowError`` when fill_size is given and the number takes up more
        bytes than fit into the block. This requires the ``overflow``
        argument to this function to be set to ``False`` otherwise, no
        error will be raised.
    """

    if number < 0:
        raise ValueError("Number must be an unsigned integer: %d" % number)

    if fill_size and chunk_size:
        raise ValueError("You can either fill or pad chunks, but not both")

    # Ensure these are integers.
    assert isinstance(number, int), "Number must be an unsigned integer, not a float."

    raw_bytes = b""

    # Pack the integer one machine word at a time into bytes.
    num = number
    word_bits, _, max_uint, pack_type = machine_size.get_word_alignment(num)
    pack_format = ">%s" % pack_type
    while num > 0:
        raw_bytes = pack(pack_format, num & max_uint) + raw_bytes
        num >>= word_bits
    # Obtain the index of the first non-zero byte.
    zero_leading = bytes_leading(raw_bytes)
    if number == 0:
        raw_bytes = b"\x00"
    # De-padding.
    raw_bytes = raw_bytes[zero_leading:]

    length = len(raw_bytes)
    if fill_size and fill_size > 0:
        if not overflow and length > fill_size:
            raise OverflowError(
                "Need %d bytes for number, but fill size is %d" % (length, fill_size)
            )
        raw_bytes = (b"\x00" * (fill_size - len(raw_bytes))) + raw_bytes
    elif chunk_size and chunk_size > 0:
        remainder = length % chunk_size
        if remainder:
            padding_size = chunk_size - remainder
            raw_bytes = "% {}s".format(length + padding_size).encode() % raw_bytes
    return raw_bytes
