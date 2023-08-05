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
from .HeightDto import HeightDto
from .MosaicPropertiesBuilder import MosaicPropertiesBuilder

class MosaicDefinitionBuilder:
    """Binary layout for mosaic definition.

    Attributes:
        startHeight: Block height.
        ownerAddress: Mosaic owner.
        revision: Revision.
        properties: Properties.
    """

    def __init__(self, startHeight: HeightDto, ownerAddress: AddressDto, revision: int, properties: MosaicPropertiesBuilder):
        """Constructor.
        Args:
            startHeight: Block height.
            ownerAddress: Mosaic owner.
            revision: Revision.
            properties: Properties.
        """
        self.startHeight = startHeight
        self.ownerAddress = ownerAddress
        self.revision = revision
        self.properties = properties


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicDefinitionBuilder:
        """Creates an instance of MosaicDefinitionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicDefinitionBuilder.
        """
        bytes_ = bytes(payload)

        startHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[startHeight.getSize():]
        ownerAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[ownerAddress.getSize():]
        revision = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        properties = MosaicPropertiesBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[properties.getSize():]
        return MosaicDefinitionBuilder(startHeight, ownerAddress, revision, properties)

    def getStartHeight(self) -> HeightDto:
        """Gets block height.
        Returns:
            Block height.
        """
        return self.startHeight

    def getOwnerAddress(self) -> AddressDto:
        """Gets mosaic owner.
        Returns:
            Mosaic owner.
        """
        return self.ownerAddress

    def getRevision(self) -> int:
        """Gets revision.
        Returns:
            Revision.
        """
        return self.revision

    def getProperties(self) -> MosaicPropertiesBuilder:
        """Gets properties.
        Returns:
            Properties.
        """
        return self.properties

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.startHeight.getSize()
        size += self.ownerAddress.getSize()
        size += 4  # revision
        size += self.properties.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.startHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.ownerAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getRevision(), 4))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.properties.serialize())  # kind:CUSTOM
        return bytes_
