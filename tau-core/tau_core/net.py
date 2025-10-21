#!/usr/bin/env python3
"""Encrypted network communication channel for tau RPC"""
import json
import sys
from Crypto.Cipher import AES

from . import config


def get_encryption_key():
    """Get encryption key from config"""
    # should be 32 bytes hex
    # https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
    default_key = "87b9b70e722d20c046c8dba8d0add1f16307fec33debffec9d001fd20dbca3ee"
    return bytes.fromhex(config.get("shared_secret", default_key))


class Channel:
    """Encrypted bidirectional communication channel"""

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def readline(self):
        """Read a line from the channel"""
        if not (line := await self.reader.readline()):
            self.writer.close()
            return None
        # Strip the newline
        return line[:-1].decode()

    async def receive(self):
        """Receive and decrypt a message"""
        if (nonce := await self.readline()) is None:
            return None
        if (ciphertext := await self.readline()) is None:
            return None
        if (tag := await self.readline()) is None:
            return None

        nonce = bytes.fromhex(nonce)
        ciphertext = bytes.fromhex(ciphertext)
        tag = bytes.fromhex(tag)

        # Decrypt
        cipher = AES.new(get_encryption_key(), AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
        except ValueError:
            print("error: key incorrect or message corrupted", file=sys.stderr)
            return None

        message = plaintext.decode()
        response = json.loads(message)
        return response

    async def send(self, obj):
        """Encrypt and send a message"""
        message = json.dumps(obj)
        data = message.encode()

        # Encrypt
        cipher = AES.new(get_encryption_key(), AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        # Encode as hex strings since the bytes might contain new lines
        nonce = nonce.hex().encode()
        ciphertext = ciphertext.hex().encode()
        tag = tag.hex().encode()

        self.writer.write(nonce + b"\n")
        self.writer.write(ciphertext + b"\n")
        self.writer.write(tag + b"\n")
        await self.writer.drain()
