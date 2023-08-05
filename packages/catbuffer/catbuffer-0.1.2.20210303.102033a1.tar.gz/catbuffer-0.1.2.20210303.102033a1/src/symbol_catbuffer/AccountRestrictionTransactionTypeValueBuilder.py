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
from .EntityTypeDto import EntityTypeDto

class AccountRestrictionTransactionTypeValueBuilder:
    """Binary layout for transaction type based account restriction.

    Attributes:
        restrictionValues: Restriction values.
    """

    def __init__(self, restrictionValues: List[EntityTypeDto]):
        """Constructor.
        Args:
            restrictionValues: Restriction values.
        """
        self.restrictionValues = restrictionValues


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountRestrictionTransactionTypeValueBuilder:
        """Creates an instance of AccountRestrictionTransactionTypeValueBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountRestrictionTransactionTypeValueBuilder.
        """
        bytes_ = bytes(payload)

        restrictionValuesCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIZE_FIELD
        bytes_ = bytes_[8:]
        restrictionValues: List[EntityTypeDto] = []  # kind:ARRAY
        for _ in range(restrictionValuesCount):
            item = EntityTypeDto.loadFromBinary(bytes_)
            restrictionValues.append(item)
            bytes_ = bytes_[item.getSize():]
        return AccountRestrictionTransactionTypeValueBuilder(restrictionValues)

    def getRestrictionValues(self) -> List[EntityTypeDto]:
        """Gets restriction values.
        Returns:
            Restriction values.
        """
        return self.restrictionValues

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 8  # restrictionValuesCount
        for _ in self.restrictionValues:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getRestrictionValues()), 8))  # kind:SIZE_FIELD
        for _ in self.restrictionValues: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        return bytes_
