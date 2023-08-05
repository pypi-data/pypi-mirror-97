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
from .BlockDurationDto import BlockDurationDto
from .Hash256Dto import Hash256Dto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

# from binascii import hexlify

class HashLockTransactionBodyBuilder:
    """Binary layout for a hash lock transaction.

    Attributes:
        mosaic: Lock mosaic.
        duration: Number of blocks for which a lock should be valid.
        hash: Lock hash.
    """
    mosaic = None # UnresolvedMosaicBuilder
    duration = BlockDurationDto().blockDuration
    hash = bytes(32)

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HashLockTransactionBodyBuilder:
        """Creates an instance of HashLockTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HashLockTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaic = UnresolvedMosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[mosaic.getSize():]
        mosaic = mosaic.as_tuple()
        duration_ = BlockDurationDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        duration = duration_.blockDuration
        bytes_ = bytes_[duration_.getSize():]
        hash_ = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        hash = hash_.hash256
        bytes_ = bytes_[hash_.getSize():]

        # create object and call
        result = HashLockTransactionBodyBuilder()
        result.mosaic = mosaic
        result.duration = duration
        result.hash = hash
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedMosaicBuilder.from_tuple(self.mosaic).getSize()
        size += BlockDurationDto(self.duration).getSize()
        size += Hash256Dto(self.hash).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicBuilder.from_tuple(self.mosaic).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('mosaic', hexlify(UnresolvedMosaicBuilder.from_tuple(self.mosaic).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, BlockDurationDto(self.duration).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('duration', hexlify(BlockDurationDto(self.duration).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, Hash256Dto(self.hash).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('hash', hexlify(Hash256Dto(self.hash).serialize())))
        return bytes_
