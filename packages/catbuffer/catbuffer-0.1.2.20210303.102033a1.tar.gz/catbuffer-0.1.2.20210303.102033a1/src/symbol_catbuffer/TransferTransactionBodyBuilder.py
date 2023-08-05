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
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

# from binascii import hexlify

class TransferTransactionBodyBuilder:
    """Binary layout for a transfer transaction.

    Attributes:
        recipientAddress: Recipient address.
        mosaics: Attached mosaics.
        message: Attached message.
    """
    recipientAddress = bytes(24)
    mosaics = []
    message = bytes()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> TransferTransactionBodyBuilder:
        """Creates an instance of TransferTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of TransferTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        recipientAddress_ = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        recipientAddress = recipientAddress_.unresolvedAddress
        bytes_ = bytes_[recipientAddress_.getSize():]
        messageSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIZE_FIELD
        bytes_ = bytes_[2:]
        mosaicsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        transferTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        transferTransactionBody_Reserved2 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]
        mosaics = []  # kind:ARRAY
        for _ in range(mosaicsCount):
            item = UnresolvedMosaicBuilder.loadFromBinary(bytes_)
            mosaics.append(item.as_tuple())
            bytes_ = bytes_[item.getSize():]
        message = GeneratorUtils.getBytes(bytes_, messageSize)  # kind:BUFFER
        bytes_ = bytes_[messageSize:]

        # create object and call
        result = TransferTransactionBodyBuilder()
        result.recipientAddress = recipientAddress
        result.mosaics = mosaics
        result.message = message
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedAddressDto(self.recipientAddress).getSize()
        size += 2  # messageSize
        size += 1  # mosaicsCount
        size += 4  # transferTransactionBody_Reserved1
        size += 1  # transferTransactionBody_Reserved2
        for _ in self.mosaics:
            size += UnresolvedMosaicBuilder.from_tuple(_).getSize()
        size += len(self.message)
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(self.recipientAddress).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('recipientAddress', hexlify(UnresolvedAddressDto(self.recipientAddress).serialize())))
        size_value = len(self.message)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 2))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('messageSize', hexlify(GeneratorUtils.uintToBuffer(size_value, 2))))
        size_value = len(self.mosaics)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('mosaicsCount', hexlify(GeneratorUtils.uintToBuffer(size_value, 1))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        # print("1. {:20s} : {}".format('transferTransactionBody_Reserved1', hexlify(GeneratorUtils.uintToBuffer(0, 4))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 1))
        # print("1. {:20s} : {}".format('transferTransactionBody_Reserved2', hexlify(GeneratorUtils.uintToBuffer(0, 1))))
        for _ in self.mosaics: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicBuilder.from_tuple(_).serialize())
            # print("6. {:20s} : {}".format('mosaics', hexlify(UnresolvedMosaicBuilder.from_tuple(_).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.message)  # kind:BUFFER
        # 4. message
        # print("4. {:20s} : {}".format('message', hexlify(self.message)))
        return bytes_
