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


class UnresolvedMosaicIdDto:
    """Unresolved mosaic id.

    Attributes:
        unresolvedMosaicId: Unresolved mosaic id.
    """
    def __init__(self, unresolvedMosaicId: int = 0):
        """Constructor.

        Args:
            unresolvedMosaicId: Unresolved mosaic id.
        """
        self.unresolvedMosaicId = unresolvedMosaicId

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> UnresolvedMosaicIdDto:
        """Creates an instance of UnresolvedMosaicIdDto from binary payload.

        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of UnresolvedMosaicIdDto.
        """
        bytes_ = bytes(payload)
        unresolvedMosaicId = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))
        return UnresolvedMosaicIdDto(unresolvedMosaicId)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 8

    def getUnresolvedMosaicId(self) -> int:
        """Gets Unresolved mosaic id.

        Returns:
            Unresolved mosaic id.
        """
        return self.unresolvedMosaicId

    def serialize(self) -> bytes:
        """Serializes self to bytes.

        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getUnresolvedMosaicId(), 8))
        return bytes_
