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


class MosaicRestrictionKeyDto:
    """Mosaic restriction key.

    Attributes:
        mosaicRestrictionKey: Mosaic restriction key.
    """
    def __init__(self, mosaicRestrictionKey: int = 0):
        """Constructor.

        Args:
            mosaicRestrictionKey: Mosaic restriction key.
        """
        self.mosaicRestrictionKey = mosaicRestrictionKey

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicRestrictionKeyDto:
        """Creates an instance of MosaicRestrictionKeyDto from binary payload.

        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicRestrictionKeyDto.
        """
        bytes_ = bytes(payload)
        mosaicRestrictionKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))
        return MosaicRestrictionKeyDto(mosaicRestrictionKey)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 8

    def getMosaicRestrictionKey(self) -> int:
        """Gets Mosaic restriction key.

        Returns:
            Mosaic restriction key.
        """
        return self.mosaicRestrictionKey

    def serialize(self) -> bytes:
        """Serializes self to bytes.

        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getMosaicRestrictionKey(), 8))
        return bytes_
