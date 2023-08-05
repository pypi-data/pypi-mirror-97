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

class ReceiptSourceBuilder:
    """Binary layout for receipt source.

    Attributes:
        primaryId: Transaction primary source (e.g. index within block).
        secondaryId: Transaction secondary source (e.g. index within aggregate).
    """

    def __init__(self, primaryId: int, secondaryId: int):
        """Constructor.
        Args:
            primaryId: Transaction primary source (e.g. index within block).
            secondaryId: Transaction secondary source (e.g. index within aggregate).
        """
        self.primaryId = primaryId
        self.secondaryId = secondaryId


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> ReceiptSourceBuilder:
        """Creates an instance of ReceiptSourceBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of ReceiptSourceBuilder.
        """
        bytes_ = bytes(payload)

        primaryId = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        secondaryId = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        return ReceiptSourceBuilder(primaryId, secondaryId)

    def getPrimaryId(self) -> int:
        """Gets transaction primary source (e.g. index within block).
        Returns:
            Transaction primary source (e.g. index within block).
        """
        return self.primaryId

    def getSecondaryId(self) -> int:
        """Gets transaction secondary source (e.g. index within aggregate).
        Returns:
            Transaction secondary source (e.g. index within aggregate).
        """
        return self.secondaryId

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 4  # primaryId
        size += 4  # secondaryId
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getPrimaryId(), 4))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getSecondaryId(), 4))  # kind:SIMPLE
        return bytes_
