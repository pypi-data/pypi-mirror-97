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
from .NamespaceAliasBuilder import NamespaceAliasBuilder
from .NamespaceIdDto import NamespaceIdDto

class NamespacePathBuilder:
    """Binary layout for a namespace path.

    Attributes:
        path: Namespace path (excluding root id).
        alias: Namespace alias.
    """

    def __init__(self, path: List[NamespaceIdDto], alias: NamespaceAliasBuilder):
        """Constructor.
        Args:
            path: Namespace path (excluding root id).
            alias: Namespace alias.
        """
        self.path = path
        self.alias = alias


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespacePathBuilder:
        """Creates an instance of NamespacePathBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespacePathBuilder.
        """
        bytes_ = bytes(payload)

        pathSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        path: List[NamespaceIdDto] = []  # kind:ARRAY
        for _ in range(pathSize):
            item = NamespaceIdDto.loadFromBinary(bytes_)
            path.append(item)
            bytes_ = bytes_[item.getSize():]
        alias = NamespaceAliasBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[alias.getSize():]
        return NamespacePathBuilder(path, alias)

    def getPath(self) -> List[NamespaceIdDto]:
        """Gets namespace path (excluding root id).
        Returns:
            Namespace path (excluding root id).
        """
        return self.path

    def getAlias(self) -> NamespaceAliasBuilder:
        """Gets namespace alias.
        Returns:
            Namespace alias.
        """
        return self.alias

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 1  # pathSize
        for _ in self.path:
            size += _.getSize()
        size += self.alias.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getPath()), 1))  # kind:SIZE_FIELD
        for _ in self.path: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.alias.serialize())  # kind:CUSTOM
        return bytes_
