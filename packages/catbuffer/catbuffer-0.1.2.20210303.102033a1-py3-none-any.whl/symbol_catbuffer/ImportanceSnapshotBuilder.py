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
from .ImportanceDto import ImportanceDto
from .ImportanceHeightDto import ImportanceHeightDto

class ImportanceSnapshotBuilder:
    """Temporal importance information.

    Attributes:
        importance: Account importance.
        height: Importance height.
    """

    def __init__(self, importance: ImportanceDto, height: ImportanceHeightDto):
        """Constructor.
        Args:
            importance: Account importance.
            height: Importance height.
        """
        self.importance = importance
        self.height = height


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> ImportanceSnapshotBuilder:
        """Creates an instance of ImportanceSnapshotBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of ImportanceSnapshotBuilder.
        """
        bytes_ = bytes(payload)

        importance = ImportanceDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[importance.getSize():]
        height = ImportanceHeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[height.getSize():]
        return ImportanceSnapshotBuilder(importance, height)

    def getImportance(self) -> ImportanceDto:
        """Gets account importance.
        Returns:
            Account importance.
        """
        return self.importance

    def getHeight(self) -> ImportanceHeightDto:
        """Gets importance height.
        Returns:
            Importance height.
        """
        return self.height

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.importance.getSize()
        size += self.height.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.importance.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.height.serialize())  # kind:CUSTOM
        return bytes_
