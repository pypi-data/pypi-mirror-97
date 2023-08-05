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
from .MosaicAddressRestrictionEntryBuilder import MosaicAddressRestrictionEntryBuilder
from .MosaicGlobalRestrictionEntryBuilder import MosaicGlobalRestrictionEntryBuilder
from .MosaicRestrictionEntryTypeDto import MosaicRestrictionEntryTypeDto
from .StateHeaderBuilder import StateHeaderBuilder

class MosaicRestrictionEntryBuilder(StateHeaderBuilder):
    """Binary layout for a mosaic restriction.

    Attributes:
        entryType: Type of restriction being placed upon the entity.
        addressEntry: Address restriction rule.
        globalEntry: Global mosaic rule.
    """

    def __init__(self, version: int, entryType: MosaicRestrictionEntryTypeDto, addressEntry: MosaicAddressRestrictionEntryBuilder, globalEntry: MosaicGlobalRestrictionEntryBuilder):
        """Constructor.
        Args:
            version: Serialization version.
            entryType: Type of restriction being placed upon the entity.
            addressEntry: Address restriction rule.
            globalEntry: Global mosaic rule.
        """
        super().__init__(version)
        self.entryType = entryType
        self.addressEntry = addressEntry
        self.globalEntry = globalEntry


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicRestrictionEntryBuilder:
        """Creates an instance of MosaicRestrictionEntryBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicRestrictionEntryBuilder.
        """
        bytes_ = bytes(payload)
        superObject = StateHeaderBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        entryType = MosaicRestrictionEntryTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[entryType.getSize():]
        addressEntry = None
        if entryType == MosaicRestrictionEntryTypeDto.ADDRESS:
            addressEntry = MosaicAddressRestrictionEntryBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[addressEntry.getSize():]
        globalEntry = None
        if entryType == MosaicRestrictionEntryTypeDto.GLOBAL:
            globalEntry = MosaicGlobalRestrictionEntryBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[globalEntry.getSize():]
        return MosaicRestrictionEntryBuilder(superObject.version, entryType, addressEntry, globalEntry)

    def getEntryType(self) -> MosaicRestrictionEntryTypeDto:
        """Gets type of restriction being placed upon the entity.
        Returns:
            Type of restriction being placed upon the entity.
        """
        return self.entryType

    def getAddressEntry(self) -> MosaicAddressRestrictionEntryBuilder:
        """Gets address restriction rule.
        Returns:
            Address restriction rule.
        """
        if not self.entryType == MosaicRestrictionEntryTypeDto.ADDRESS:
            raise Exception('entryType is not set to ADDRESS.')
        return self.addressEntry

    def getGlobalEntry(self) -> MosaicGlobalRestrictionEntryBuilder:
        """Gets global mosaic rule.
        Returns:
            Global mosaic rule.
        """
        if not self.entryType == MosaicRestrictionEntryTypeDto.GLOBAL:
            raise Exception('entryType is not set to GLOBAL.')
        return self.globalEntry

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.entryType.getSize()
        if self.entryType == MosaicRestrictionEntryTypeDto.ADDRESS:
            size += self.addressEntry.getSize()
        if self.entryType == MosaicRestrictionEntryTypeDto.GLOBAL:
            size += self.globalEntry.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.entryType.serialize())  # kind:CUSTOM
        if self.entryType == MosaicRestrictionEntryTypeDto.ADDRESS:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.addressEntry.serialize())  # kind:CUSTOM
        if self.entryType == MosaicRestrictionEntryTypeDto.GLOBAL:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.globalEntry.serialize())  # kind:CUSTOM
        return bytes_
