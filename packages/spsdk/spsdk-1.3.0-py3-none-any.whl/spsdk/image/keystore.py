#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module provides support for KeyStore used in MasterBootImage."""

from Crypto.Cipher import AES

from spsdk.utils.easy_enum import Enum


class KeySourceType(Enum):
    """Device key source."""
    OTP = (0, 'Device keys stored in OTP')
    KEYSTORE = (1, 'Device keys stored in KeyStore')


class KeyStore:
    """Provide info about KeyStore for MaterBootImage."""
    # size of key store in bytes
    KEY_STORE_SIZE = 1424  # TODO size can be device-specific, the current value is valid for RT5xx and RT6xx

    @property
    def key_source(self) -> KeySourceType:
        """Device key source."""
        return self._key_source

    def __init__(self, key_source: KeySourceType, key_store: bytes = None) -> None:
        """Initialize Keystore.

        :param key_source: device key source
        :param key_store: initial content of the key store in the bootable image; None if empty
        :raises ValueError: if invalid key-store size
        """
        if key_store:
            if len(key_store) != self.KEY_STORE_SIZE:
                raise ValueError(f"Invalid key-store size, expected is {str(self.KEY_STORE_SIZE)} bytes")
            assert key_source == KeySourceType.KEYSTORE, "KeyStore can be initialized only if key_source == KEYSTORE"

        self._key_source = key_source
        self._key_store = key_store

    def export(self) -> bytes:
        """Binary key store content; empty bytes for empty key-store."""
        return self._key_store if self._key_store else bytes()

    def info(self) -> str:
        """Information about key store in text form."""
        msg = f"Device key source:    {KeySourceType.name(self.key_source)}\n" + \
              f"Device key store len: {str(len(self.export()))}"
        return msg

    @staticmethod
    def derive_hmac_key(hmac_key: bytes) -> bytes:
        """Derive HMAC from master or user key.

        :param hmac_key: either master-key (for key_source == OTP) or user key (for key_source == KEYSTORE)
        :return: key used for image header authentication in LoadToRam images
        """
        assert len(hmac_key) == 32
        aes = AES.new(hmac_key, AES.MODE_ECB)
        return aes.encrypt(bytes([0] * 16))

    @staticmethod
    def derive_enc_image_key(master_key: bytes) -> bytes:
        """Derive "enc_image_key" from master key.

        :param master_key: stored in OTP
        :return: key used to decrypt encrypted images during boot
        """
        assert len(master_key) == 32
        aes = AES.new(master_key, AES.MODE_ECB)
        return aes.encrypt(bytes([1] + [0] * 15 + [2] + [0] * 15))

    @staticmethod
    def derive_sb_kek_key(master_key: bytes) -> bytes:
        """Derive SBKEK key from master key.

        :param master_key: 32 bytes key, stored in OTP
        :return: encryption key to handle SB2 file (update capsule)
        """
        assert len(master_key) == 32
        aes = AES.new(master_key, AES.MODE_ECB)
        return aes.encrypt(bytes([3] + [0] * 15 + [4] + [0] * 15))

    @staticmethod
    def derive_otfad_kek_key(master_key: bytes, otfad_input: bytes) -> bytes:
        """Derive OTFAD KEK key from master key and OTFAD input.

        :param master_key: 32 bytes key, stored in OTP
        :param otfad_input: 16 bytes input, stored in OTP
        :return: OTFAD encryption key for FLASH encryption/decryption
        """
        assert len(master_key) == 32
        assert len(otfad_input) == 16
        aes = AES.new(master_key, AES.MODE_ECB)
        return aes.encrypt(otfad_input)
