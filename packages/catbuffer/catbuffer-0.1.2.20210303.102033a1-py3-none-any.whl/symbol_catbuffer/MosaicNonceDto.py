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


class MosaicNonceDto:
    """Mosaic nonce.

    Attributes:
        mosaicNonce: Mosaic nonce.
    """
    def __init__(self, mosaicNonce: int = 0):
        """Constructor.

        Args:
            mosaicNonce: Mosaic nonce.
        """
        self.mosaicNonce = mosaicNonce

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicNonceDto:
        """Creates an instance of MosaicNonceDto from binary payload.

        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicNonceDto.
        """
        bytes_ = bytes(payload)
        mosaicNonce = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        return MosaicNonceDto(mosaicNonce)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 4

    def getMosaicNonce(self) -> int:
        """Gets Mosaic nonce.

        Returns:
            Mosaic nonce.
        """
        return self.mosaicNonce

    def serialize(self) -> bytes:
        """Serializes self to bytes.

        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMosaicNonce(), 4))
        return bytes_
