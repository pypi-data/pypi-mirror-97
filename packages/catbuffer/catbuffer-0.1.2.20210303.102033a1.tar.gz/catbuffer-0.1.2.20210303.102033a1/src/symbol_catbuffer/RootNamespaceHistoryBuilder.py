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
from .AddressDto import AddressDto
from .NamespaceAliasBuilder import NamespaceAliasBuilder
from .NamespaceIdDto import NamespaceIdDto
from .NamespaceLifetimeBuilder import NamespaceLifetimeBuilder
from .NamespacePathBuilder import NamespacePathBuilder
from .StateHeaderBuilder import StateHeaderBuilder

class RootNamespaceHistoryBuilder(StateHeaderBuilder):
    """Binary layout for non-historical root namespace history.

    Attributes:
        id: Id of the root namespace history.
        ownerAddress: Namespace owner address.
        lifetime: Lifetime in blocks.
        rootAlias: Root namespace alias.
        paths: Save child sub-namespace paths.
    """

    def __init__(self, version: int, id: NamespaceIdDto, ownerAddress: AddressDto, lifetime: NamespaceLifetimeBuilder, rootAlias: NamespaceAliasBuilder, paths: List[NamespacePathBuilder]):
        """Constructor.
        Args:
            version: Serialization version.
            id: Id of the root namespace history.
            ownerAddress: Namespace owner address.
            lifetime: Lifetime in blocks.
            rootAlias: Root namespace alias.
            paths: Save child sub-namespace paths.
        """
        super().__init__(version)
        self.id = id
        self.ownerAddress = ownerAddress
        self.lifetime = lifetime
        self.rootAlias = rootAlias
        self.paths = paths


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> RootNamespaceHistoryBuilder:
        """Creates an instance of RootNamespaceHistoryBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of RootNamespaceHistoryBuilder.
        """
        bytes_ = bytes(payload)
        superObject = StateHeaderBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        id = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[id.getSize():]
        ownerAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[ownerAddress.getSize():]
        lifetime = NamespaceLifetimeBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[lifetime.getSize():]
        rootAlias = NamespaceAliasBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[rootAlias.getSize():]
        childrenCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIZE_FIELD
        bytes_ = bytes_[8:]
        paths: List[NamespacePathBuilder] = []  # kind:ARRAY
        for _ in range(childrenCount):
            item = NamespacePathBuilder.loadFromBinary(bytes_)
            paths.append(item)
            bytes_ = bytes_[item.getSize():]
        return RootNamespaceHistoryBuilder(superObject.version, id, ownerAddress, lifetime, rootAlias, paths)

    def getId(self) -> NamespaceIdDto:
        """Gets id of the root namespace history.
        Returns:
            Id of the root namespace history.
        """
        return self.id

    def getOwnerAddress(self) -> AddressDto:
        """Gets namespace owner address.
        Returns:
            Namespace owner address.
        """
        return self.ownerAddress

    def getLifetime(self) -> NamespaceLifetimeBuilder:
        """Gets lifetime in blocks.
        Returns:
            Lifetime in blocks.
        """
        return self.lifetime

    def getRootAlias(self) -> NamespaceAliasBuilder:
        """Gets root namespace alias.
        Returns:
            Root namespace alias.
        """
        return self.rootAlias

    def getPaths(self) -> List[NamespacePathBuilder]:
        """Gets save child sub-namespace paths.
        Returns:
            Save child sub-namespace paths.
        """
        return self.paths

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.id.getSize()
        size += self.ownerAddress.getSize()
        size += self.lifetime.getSize()
        size += self.rootAlias.getSize()
        size += 8  # childrenCount
        for _ in self.paths:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.id.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.ownerAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.lifetime.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.rootAlias.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getPaths()), 8))  # kind:SIZE_FIELD
        for _ in self.paths: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        return bytes_
