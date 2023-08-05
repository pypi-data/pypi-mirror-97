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


class FinalizationEpochDto:
    """Finalization epoch.

    Attributes:
        finalizationEpoch: Finalization epoch.
    """
    def __init__(self, finalizationEpoch: int = 0):
        """Constructor.

        Args:
            finalizationEpoch: Finalization epoch.
        """
        self.finalizationEpoch = finalizationEpoch

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> FinalizationEpochDto:
        """Creates an instance of FinalizationEpochDto from binary payload.

        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of FinalizationEpochDto.
        """
        bytes_ = bytes(payload)
        finalizationEpoch = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))
        return FinalizationEpochDto(finalizationEpoch)

    @classmethod
    def getSize(cls) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        return 4

    def getFinalizationEpoch(self) -> int:
        """Gets Finalization epoch.

        Returns:
            Finalization epoch.
        """
        return self.finalizationEpoch

    def serialize(self) -> bytes:
        """Serializes self to bytes.

        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getFinalizationEpoch(), 4))
        return bytes_
