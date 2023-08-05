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
from .AccountRestrictionsInfoBuilder import AccountRestrictionsInfoBuilder
from .AddressDto import AddressDto
from .StateHeaderBuilder import StateHeaderBuilder

class AccountRestrictionsBuilder(StateHeaderBuilder):
    """Binary layout for account restrictions.

    Attributes:
        address: Address on which restrictions are placed.
        restrictions: Account restrictions.
    """

    def __init__(self, version: int, address: AddressDto, restrictions: List[AccountRestrictionsInfoBuilder]):
        """Constructor.
        Args:
            version: Serialization version.
            address: Address on which restrictions are placed.
            restrictions: Account restrictions.
        """
        super().__init__(version)
        self.address = address
        self.restrictions = restrictions


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountRestrictionsBuilder:
        """Creates an instance of AccountRestrictionsBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountRestrictionsBuilder.
        """
        bytes_ = bytes(payload)
        superObject = StateHeaderBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        address = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[address.getSize():]
        restrictionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIZE_FIELD
        bytes_ = bytes_[8:]
        restrictions: List[AccountRestrictionsInfoBuilder] = []  # kind:ARRAY
        for _ in range(restrictionsCount):
            item = AccountRestrictionsInfoBuilder.loadFromBinary(bytes_)
            restrictions.append(item)
            bytes_ = bytes_[item.getSize():]
        return AccountRestrictionsBuilder(superObject.version, address, restrictions)

    def getAddress(self) -> AddressDto:
        """Gets address on which restrictions are placed.
        Returns:
            Address on which restrictions are placed.
        """
        return self.address

    def getRestrictions(self) -> List[AccountRestrictionsInfoBuilder]:
        """Gets account restrictions.
        Returns:
            Account restrictions.
        """
        return self.restrictions

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.address.getSize()
        size += 8  # restrictionsCount
        for _ in self.restrictions:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.address.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getRestrictions()), 8))  # kind:SIZE_FIELD
        for _ in self.restrictions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        return bytes_
