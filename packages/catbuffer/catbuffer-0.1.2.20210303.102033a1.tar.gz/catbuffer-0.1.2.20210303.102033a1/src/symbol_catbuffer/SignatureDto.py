#!/usr/bin/python
"""
    Copyright (c) 2016-2019, Jaguar0625, gimre, BloodyRookie, Tech Bureau, Corp.
    Copyright (c) 2020-present, Jaguar0625, gimre, BloodyRookie.

    This file is part of Catapult.

    Catapult is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Catapult is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Catapult. If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0622,W0612,C0301,R0904

from __future__ import annotations
from .GeneratorUtils import GeneratorUtils


class SignatureDto:
    """Signature.

    Attributes:
        signature: Signature.
    """
    def __init__(self, signature: bytes = bytes(64)):
        """Constructor.

        Args:
            signature: Signature.
        """
        assert len(signature) == 64, 'required argument bytes({})'.format(64)
        self.signature = signature

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SignatureDto:
        """Creates an instance of SignatureDto from binary payload.

        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SignatureDto.
        """
        bytes_ = bytes(payload)
        signature = GeneratorUtils.getBytes(bytes_, 64)
        return SignatureDto(signature)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 64

    def getSignature(self) -> bytes:
        """Gets Signature.

        Returns:
            Signature.
        """
        return self.signature

    def serialize(self) -> bytes:
        """Serializes self to bytes.

        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.signature)
        return bytes_
