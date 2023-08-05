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
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicBuilder import UnresolvedMosaicBuilder

# from binascii import hexlify

class SecretLockTransactionBodyBuilder:
    """Binary layout for a secret lock transaction.

    Attributes:
        recipientAddress: Locked mosaic recipient address.
        secret: Secret.
        mosaic: Locked mosaic.
        duration: Number of blocks for which a lock should be valid.
        hashAlgorithm: Hash algorithm.
    """
    recipientAddress = bytes(24)
    secret = bytes(32)
    mosaic = None # UnresolvedMosaicBuilder
    duration = BlockDurationDto().blockDuration
    hashAlgorithm = LockHashAlgorithmDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretLockTransactionBodyBuilder:
        """Creates an instance of SecretLockTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretLockTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        recipientAddress_ = UnresolvedAddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        recipientAddress = recipientAddress_.unresolvedAddress
        bytes_ = bytes_[recipientAddress_.getSize():]
        secret_ = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        secret = secret_.hash256
        bytes_ = bytes_[secret_.getSize():]
        mosaic = UnresolvedMosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[mosaic.getSize():]
        mosaic = mosaic.as_tuple()
        duration_ = BlockDurationDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        duration = duration_.blockDuration
        bytes_ = bytes_[duration_.getSize():]
        hashAlgorithm_ = LockHashAlgorithmDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        hashAlgorithm = hashAlgorithm_.value
        bytes_ = bytes_[hashAlgorithm_.getSize():]

        # create object and call
        result = SecretLockTransactionBodyBuilder()
        result.recipientAddress = recipientAddress
        result.secret = secret
        result.mosaic = mosaic
        result.duration = duration
        result.hashAlgorithm = hashAlgorithm
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedAddressDto(self.recipientAddress).getSize()
        size += Hash256Dto(self.secret).getSize()
        size += UnresolvedMosaicBuilder.from_tuple(self.mosaic).getSize()
        size += BlockDurationDto(self.duration).getSize()
        size += LockHashAlgorithmDto(self.hashAlgorithm).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(self.recipientAddress).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('recipientAddress', hexlify(UnresolvedAddressDto(self.recipientAddress).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, Hash256Dto(self.secret).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('secret', hexlify(Hash256Dto(self.secret).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicBuilder.from_tuple(self.mosaic).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('mosaic', hexlify(UnresolvedMosaicBuilder.from_tuple(self.mosaic).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, BlockDurationDto(self.duration).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('duration', hexlify(BlockDurationDto(self.duration).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, LockHashAlgorithmDto(self.hashAlgorithm).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('hashAlgorithm', hexlify(LockHashAlgorithmDto(self.hashAlgorithm).serialize())))
        return bytes_
