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

from .GeneratorUtils import GeneratorUtils
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

# from binascii import hexlify

class MosaicAddressRestrictionTransactionBodyBuilder:
    """Binary layout for a mosaic address restriction transaction.

    Attributes:
        mosaicId: Identifier of the mosaic to which the restriction applies.
        restrictionKey: Restriction key.
        previousRestrictionValue: Previous restriction value.
        newRestrictionValue: New restriction value.
        targetAddress: Address being restricted.
    """
    mosaicId = UnresolvedMosaicIdDto().unresolvedMosaicId
    restrictionKey = int()
    previousRestrictionValue = int()
    newRestrictionValue = int()
    targetAddress = bytes(24)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicAddressRestrictionTransactionBodyBuilder:
        """Creates an instance of MosaicAddressRestrictionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicAddressRestrictionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaicId_ = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        mosaicId = mosaicId_.unresolvedMosaicId
        bytes_ = bytes_[mosaicId_.getSize():]
        restrictionKey = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        previousRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        newRestrictionValue = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        targetAddress_ = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        targetAddress = targetAddress_.unresolvedAddress
        bytes_ = bytes_[targetAddress_.getSize():]

        # create object and call
        result = MosaicAddressRestrictionTransactionBodyBuilder()
        result.mosaicId = mosaicId
        result.restrictionKey = restrictionKey
        result.previousRestrictionValue = previousRestrictionValue
        result.newRestrictionValue = newRestrictionValue
        result.targetAddress = targetAddress
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedMosaicIdDto(self.mosaicId).getSize()
        size += 8  # restrictionKey
        size += 8  # previousRestrictionValue
        size += 8  # newRestrictionValue
        size += UnresolvedAddressDto(self.targetAddress).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicIdDto(self.mosaicId).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('mosaicId', hexlify(UnresolvedMosaicIdDto(self.mosaicId).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.restrictionKey, 8))  # serial_kind:SIMPLE
        # print("2. {:20s} : {}".format('restrictionKey', hexlify(GeneratorUtils.uintToBuffer(self.restrictionKey, 8))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.previousRestrictionValue, 8))  # serial_kind:SIMPLE
        # print("2. {:20s} : {}".format('previousRestrictionValue', hexlify(GeneratorUtils.uintToBuffer(self.previousRestrictionValue, 8))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.newRestrictionValue, 8))  # serial_kind:SIMPLE
        # print("2. {:20s} : {}".format('newRestrictionValue', hexlify(GeneratorUtils.uintToBuffer(self.newRestrictionValue, 8))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(self.targetAddress).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('targetAddress', hexlify(UnresolvedAddressDto(self.targetAddress).serialize())))
        return bytes_
