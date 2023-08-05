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

# pylint: disable=unused-import

from typing import List
from .GeneratorUtils import GeneratorUtils
from .AccountRestrictionFlagsDto import AccountRestrictionFlagsDto
from .UnresolvedAddressDto import UnresolvedAddressDto

# from binascii import hexlify

class AccountAddressRestrictionTransactionBodyBuilder:
    """Binary layout for an account address restriction transaction.

    Attributes:
        restrictionFlags: Account restriction flags.
        restrictionAdditions: Account restriction additions.
        restrictionDeletions: Account restriction deletions.
    """
    restrictionFlags = []
    restrictionAdditions = []
    restrictionDeletions = []

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountAddressRestrictionTransactionBodyBuilder:
        """Creates an instance of AccountAddressRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountAddressRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        restrictionFlags = AccountRestrictionFlagsDto.bytesToFlags(bytes_, 2)  # kind:FLAGS
        bytes_ = bytes_[2:]
        restrictionAdditionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        restrictionDeletionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        accountRestrictionTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        restrictionAdditions = []  # kind:ARRAY
        for _ in range(restrictionAdditionsCount):
            item = UnresolvedAddressDto.loadFromBinary(bytes_)
            restrictionAdditions.append(item.unresolvedAddress)
            bytes_ = bytes_[item.getSize():]
        restrictionDeletions = []  # kind:ARRAY
        for _ in range(restrictionDeletionsCount):
            item = UnresolvedAddressDto.loadFromBinary(bytes_)
            restrictionDeletions.append(item.unresolvedAddress)
            bytes_ = bytes_[item.getSize():]

        # create object and call
        result = AccountAddressRestrictionTransactionBodyBuilder()
        result.restrictionFlags = restrictionFlags
        result.restrictionAdditions = restrictionAdditions
        result.restrictionDeletions = restrictionDeletions
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 2  # restrictionFlags
        size += 1  # restrictionAdditionsCount
        size += 1  # restrictionDeletionsCount
        size += 4  # accountRestrictionTransactionBody_Reserved1
        for _ in self.restrictionAdditions:
            size += UnresolvedAddressDto(_).getSize()
        for _ in self.restrictionDeletions:
            size += UnresolvedAddressDto(_).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(AccountRestrictionFlagsDto.flagsToInt(self.restrictionFlags), 2))  # kind:FLAGS
        # print("9. {:20s}".format('restrictionFlags'))
        size_value = len(self.restrictionAdditions)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('restrictionAdditionsCount', hexlify(GeneratorUtils.uintToBuffer(size_value, 1))))
        size_value = len(self.restrictionDeletions)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('restrictionDeletionsCount', hexlify(GeneratorUtils.uintToBuffer(size_value, 1))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        # print("1. {:20s} : {}".format('accountRestrictionTransactionBody_Reserved1', hexlify(GeneratorUtils.uintToBuffer(0, 4))))
        for _ in self.restrictionAdditions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(_).serialize())
            # print("6. {:20s} : {}".format('restrictionAdditions', hexlify(UnresolvedAddressDto(_).serialize())))
        for _ in self.restrictionDeletions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(_).serialize())
            # print("6. {:20s} : {}".format('restrictionDeletions', hexlify(UnresolvedAddressDto(_).serialize())))
        return bytes_
