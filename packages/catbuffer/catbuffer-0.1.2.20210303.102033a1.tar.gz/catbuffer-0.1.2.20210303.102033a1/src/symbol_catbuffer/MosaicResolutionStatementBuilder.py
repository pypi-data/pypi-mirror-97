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
from typing import List
from .GeneratorUtils import GeneratorUtils
from .MosaicResolutionEntryBuilder import MosaicResolutionEntryBuilder
from .ReceiptBuilder import ReceiptBuilder
from .ReceiptTypeDto import ReceiptTypeDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

class MosaicResolutionStatementBuilder(ReceiptBuilder):
    """Binary layout for a mosaic resolution statement.

    Attributes:
        unresolved: Unresolved mosaic.
        resolutionEntries: Resolution entries.
    """

    def __init__(self, version: int, type: ReceiptTypeDto, unresolved: UnresolvedMosaicIdDto, resolutionEntries: List[MosaicResolutionEntryBuilder]):
        """Constructor.
        Args:
            version: Receipt version.
            type: Receipt type.
            unresolved: Unresolved mosaic.
            resolutionEntries: Resolution entries.
        """
        super().__init__(version, type)
        self.unresolved = unresolved
        self.resolutionEntries = resolutionEntries


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicResolutionStatementBuilder:
        """Creates an instance of MosaicResolutionStatementBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicResolutionStatementBuilder.
        """
        bytes_ = bytes(payload)
        superObject = ReceiptBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        unresolved = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[unresolved.getSize():]
        resolutionEntries: List[MosaicResolutionEntryBuilder] = []
        bytes_ = GeneratorUtils.loadFromBinary(MosaicResolutionEntryBuilder, resolutionEntries, bytes_, len(bytes_))
        return MosaicResolutionStatementBuilder(superObject.version, superObject.type, unresolved, resolutionEntries)

    def getUnresolved(self) -> UnresolvedMosaicIdDto:
        """Gets unresolved mosaic.
        Returns:
            Unresolved mosaic.
        """
        return self.unresolved

    def getResolutionEntries(self) -> List[MosaicResolutionEntryBuilder]:
        """Gets resolution entries.
        Returns:
            Resolution entries.
        """
        return self.resolutionEntries

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.unresolved.getSize()
        for _ in self.resolutionEntries:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.unresolved.serialize())  # kind:CUSTOM
        for _ in self.resolutionEntries: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        return bytes_
