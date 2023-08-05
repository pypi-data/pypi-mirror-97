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
from .AddressDto import AddressDto
from .MetadataTypeDto import MetadataTypeDto
from .MetadataValueBuilder import MetadataValueBuilder
from .ScopedMetadataKeyDto import ScopedMetadataKeyDto
from .StateHeaderBuilder import StateHeaderBuilder

class MetadataEntryBuilder(StateHeaderBuilder):
    """Binary layout of a metadata entry.

    Attributes:
        sourceAddress: Metadata source address (provider).
        targetAddress: Metadata target address.
        scopedMetadataKey: Metadata key scoped to source, target and type.
        targetId: Target id.
        metadataType: Metadata type.
        value: Value.
    """

    def __init__(self, version: int, sourceAddress: AddressDto, targetAddress: AddressDto, scopedMetadataKey: ScopedMetadataKeyDto, targetId: int, metadataType: MetadataTypeDto, value: MetadataValueBuilder):
        """Constructor.
        Args:
            version: Serialization version.
            sourceAddress: Metadata source address (provider).
            targetAddress: Metadata target address.
            scopedMetadataKey: Metadata key scoped to source, target and type.
            targetId: Target id.
            metadataType: Metadata type.
            value: Value.
        """
        super().__init__(version)
        self.sourceAddress = sourceAddress
        self.targetAddress = targetAddress
        self.scopedMetadataKey = scopedMetadataKey
        self.targetId = targetId
        self.metadataType = metadataType
        self.value = value


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MetadataEntryBuilder:
        """Creates an instance of MetadataEntryBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MetadataEntryBuilder.
        """
        bytes_ = bytes(payload)
        superObject = StateHeaderBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        sourceAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[sourceAddress.getSize():]
        targetAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[targetAddress.getSize():]
        scopedMetadataKey = ScopedMetadataKeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[scopedMetadataKey.getSize():]
        targetId = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        metadataType = MetadataTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[metadataType.getSize():]
        value = MetadataValueBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[value.getSize():]
        return MetadataEntryBuilder(superObject.version, sourceAddress, targetAddress, scopedMetadataKey, targetId, metadataType, value)

    def getSourceAddress(self) -> AddressDto:
        """Gets metadata source address (provider).
        Returns:
            Metadata source address (provider).
        """
        return self.sourceAddress

    def getTargetAddress(self) -> AddressDto:
        """Gets metadata target address.
        Returns:
            Metadata target address.
        """
        return self.targetAddress

    def getScopedMetadataKey(self) -> ScopedMetadataKeyDto:
        """Gets metadata key scoped to source, target and type.
        Returns:
            Metadata key scoped to source, target and type.
        """
        return self.scopedMetadataKey

    def getTargetId(self) -> int:
        """Gets target id.
        Returns:
            Target id.
        """
        return self.targetId

    def getMetadataType(self) -> MetadataTypeDto:
        """Gets metadata type.
        Returns:
            Metadata type.
        """
        return self.metadataType

    def getValue(self) -> MetadataValueBuilder:
        """Gets value.
        Returns:
            Value.
        """
        return self.value

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.sourceAddress.getSize()
        size += self.targetAddress.getSize()
        size += self.scopedMetadataKey.getSize()
        size += 8  # targetId
        size += self.metadataType.getSize()
        size += self.value.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.sourceAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.targetAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.scopedMetadataKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getTargetId(), 8))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.metadataType.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.value.serialize())  # kind:CUSTOM
        return bytes_
