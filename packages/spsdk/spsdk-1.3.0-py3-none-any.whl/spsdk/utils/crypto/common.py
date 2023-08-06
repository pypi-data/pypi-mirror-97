#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2019-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Common cryptographic functions."""
import math
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicNumbers
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.x509 import Certificate

from .abstract import BackendClass
from .backend_openssl import openssl_backend


def crypto_backend() -> BackendClass:
    """Return default crypto backend instance."""
    return openssl_backend


class Counter:
    """AES counter with specified counter byte ordering and customizable increment."""

    @property
    def value(self) -> bytes:
        """Initial vector for AES encryption."""
        return self._nonce + self._ctr.to_bytes(4, self._ctr_byteorder_encoding)

    def __init__(self, nonce: bytes, ctr_value: int = None, ctr_byteorder_encoding: str = 'little'):
        """Constructor.

        :param nonce: last for bytes are used as initial value for counter
        :param ctr_value: counter initial value; it is added to counter value retrieved from nonce
        :param ctr_byteorder_encoding: way how the counter is encoded into output value: either 'little' or 'big'
        """
        assert isinstance(nonce, bytes) and len(nonce) == 16
        assert ctr_byteorder_encoding in ['little', 'big']
        self._nonce = nonce[:-4]
        self._ctr_byteorder_encoding = ctr_byteorder_encoding
        self._ctr = int.from_bytes(nonce[-4:], ctr_byteorder_encoding)
        if ctr_value is not None:
            self._ctr += ctr_value

    def increment(self, value: int = 1) -> None:
        """Increment counter by specified value.

        :param value: to add to counter
        """
        self._ctr += value


# TODO refactor: This should be replaced by SecBootBlckSize.to_num_blocks
def calc_cypher_block_count(size: int) -> int:
    """Calculate the amount if cypher blocks.

    :param size: Number of bytes for the cypher area
    :return: Number of blocks covering the cypher area
    """
    return (size + 15) // 16


# TODO refactor: this should not be part of the crypto module
def swap16(x: int) -> int:
    """Swap bytes in half word (16bit).

    :param x: Original number
    :return: Number with swapped bytes
    """
    assert 0 <= x <= 0xFFFF
    return ((x << 8) & 0xFF00) | ((x >> 8) & 0x00FF)


# TODO refactor: this should not be part of the crypto module
def pack_timestamp(value: datetime) -> int:
    """Converts datetime to millisecond since 1.1.2000.

    :param value: datetime to be converted
    :return: number of milliseconds since 1.1.2000  00:00:00; 64-bit integer
    """
    assert isinstance(value, datetime)
    start = datetime(2000, 1, 1, 0, 0, 0, 0).timestamp()
    result = int((value.timestamp() - start) * 1000000)
    assert 0 <= result <= 0xFFFFFFFFFFFFFFFF
    return result


# TODO refactor: this should not be part of the crypto module
def unpack_timestamp(value: int) -> datetime:
    """Converts timestamp in millisec into datetime.

    :param value: number of milliseconds since 1.1.2000  00:00:00; 64-bit integer
    :return: corresponding datetime
    """
    assert isinstance(value, int)
    assert 0 <= value <= 0xFFFFFFFFFFFFFFFF
    start = int(datetime(2000, 1, 1, 0, 0, 0, 0).timestamp() * 1000000)
    return datetime.fromtimestamp((start + value) / 1000000)


def matches_key_and_cert(priv_key: bytes, cert: Certificate) -> bool:
    """Verify that given private key matches the public certificate.

    :param priv_key: to be tested; decrypted binary data in PEM format
    :param cert: to be used for verification
    :return: True if yes; False otherwise
    """
    signature = crypto_backend().rsa_sign(priv_key, bytes())
    assert isinstance(cert, Certificate)
    cert_pub_key = cert.public_key()  # public key of last certificate
    assert isinstance(cert_pub_key, RSAPublicKey)
    return crypto_backend().rsa_verify(
        cert_pub_key.public_numbers().n, cert_pub_key.public_numbers().e, signature, bytes()
    )


def serialize_ecc_signature(signature: bytes, coordinate_length: int) -> bytes:
    """Re-format ECC ANS.1 DER signature into the format used by ROM code."""
    r, s = utils.decode_dss_signature(signature)

    #TODO: dirty hack, this needs fixing!
    min_len = math.ceil(r.bit_length() / 8)
    if min_len > coordinate_length:
        coordinate_length = 48

    r_bytes = r.to_bytes(coordinate_length, 'big')
    s_bytes = s.to_bytes(coordinate_length, 'big')
    return r_bytes + s_bytes


def ecc_public_numbers_to_bytes(public_numbers: EllipticCurvePublicNumbers, length: int = None) -> bytes:
    """Converts public numbers from ECC key into bytes.

    :param public_numbers: instance of ecc public numbers
    :param length: length of bytes object to use
    :return: bytes representation
    """
    x = public_numbers.x
    y = public_numbers.y
    length = length or math.ceil(x.bit_length() / 8)
    x_bytes = x.to_bytes(length, 'big')
    y_bytes = y.to_bytes(length, 'big')
    return x_bytes + y_bytes
