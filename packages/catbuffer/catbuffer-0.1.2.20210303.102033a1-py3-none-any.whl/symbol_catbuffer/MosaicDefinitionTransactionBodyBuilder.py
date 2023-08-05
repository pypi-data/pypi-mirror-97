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
from .BlockDurationDto import BlockDurationDto
from .MosaicFlagsDto import MosaicFlagsDto
from .MosaicIdDto import MosaicIdDto
from .MosaicNonceDto import MosaicNonceDto

# from binascii import hexlify

class MosaicDefinitionTransactionBodyBuilder:
    """Binary layout for a mosaic definition transaction.

    Attributes:
        id: Mosaic identifier.
        duration: Mosaic duration.
        nonce: Mosaic nonce.
        flags: Mosaic flags.
        divisibility: Mosaic divisibility.
    """
    id = MosaicIdDto().mosaicId
    duration = BlockDurationDto().blockDuration
    nonce = MosaicNonceDto().mosaicNonce
    flags = []
    divisibility = int()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicDefinitionTransactionBodyBuilder:
        """Creates an instance of MosaicDefinitionTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicDefinitionTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        id_ = MosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        id = id_.mosaicId
        bytes_ = bytes_[id_.getSize():]
        duration_ = BlockDurationDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        duration = duration_.blockDuration
        bytes_ = bytes_[duration_.getSize():]
        nonce_ = MosaicNonceDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        nonce = nonce_.mosaicNonce
        bytes_ = bytes_[nonce_.getSize():]
        flags = MosaicFlagsDto.bytesToFlags(bytes_, 1)  # kind:FLAGS
        bytes_ = bytes_[1:]
        divisibility = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]

        # create object and call
        result = MosaicDefinitionTransactionBodyBuilder()
        result.id = id
        result.duration = duration
        result.nonce = nonce
        result.flags = flags
        result.divisibility = divisibility
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += MosaicIdDto(self.id).getSize()
        size += BlockDurationDto(self.duration).getSize()
        size += MosaicNonceDto(self.nonce).getSize()
        size += 1  # flags
        size += 1  # divisibility
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, MosaicIdDto(self.id).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('id', hexlify(MosaicIdDto(self.id).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, BlockDurationDto(self.duration).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('duration', hexlify(BlockDurationDto(self.duration).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, MosaicNonceDto(self.nonce).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('nonce', hexlify(MosaicNonceDto(self.nonce).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(MosaicFlagsDto.flagsToInt(self.flags), 1))  # kind:FLAGS
        # print("9. {:20s}".format('flags'))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.divisibility, 1))  # serial_kind:SIMPLE
        # print("2. {:20s} : {}".format('divisibility', hexlify(GeneratorUtils.uintToBuffer(self.divisibility, 1))))
        return bytes_
