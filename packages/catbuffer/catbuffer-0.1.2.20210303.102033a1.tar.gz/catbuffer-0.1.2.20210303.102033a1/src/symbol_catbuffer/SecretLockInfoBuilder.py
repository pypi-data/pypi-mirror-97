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
from .Hash256Dto import Hash256Dto
from .HeightDto import HeightDto
from .LockHashAlgorithmDto import LockHashAlgorithmDto
from .LockStatusDto import LockStatusDto
from .MosaicBuilder import MosaicBuilder
from .StateHeaderBuilder import StateHeaderBuilder

class SecretLockInfoBuilder(StateHeaderBuilder):
    """Binary layout for serialized lock transaction.

    Attributes:
        ownerAddress: Owner address.
        mosaic: Mosaic associated with lock.
        endHeight: Height at which the lock expires.
        status: Flag indicating whether or not the lock was already used.
        hashAlgorithm: Hash algorithm.
        secret: Transaction secret.
        recipient: Transaction recipient.
    """

    def __init__(self, version: int, ownerAddress: AddressDto, mosaic: MosaicBuilder, endHeight: HeightDto, status: LockStatusDto, hashAlgorithm: LockHashAlgorithmDto, secret: Hash256Dto, recipient: AddressDto):
        """Constructor.
        Args:
            version: Serialization version.
            ownerAddress: Owner address.
            mosaic: Mosaic associated with lock.
            endHeight: Height at which the lock expires.
            status: Flag indicating whether or not the lock was already used.
            hashAlgorithm: Hash algorithm.
            secret: Transaction secret.
            recipient: Transaction recipient.
        """
        super().__init__(version)
        self.ownerAddress = ownerAddress
        self.mosaic = mosaic
        self.endHeight = endHeight
        self.status = status
        self.hashAlgorithm = hashAlgorithm
        self.secret = secret
        self.recipient = recipient


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> SecretLockInfoBuilder:
        """Creates an instance of SecretLockInfoBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of SecretLockInfoBuilder.
        """
        bytes_ = bytes(payload)
        superObject = StateHeaderBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        ownerAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[ownerAddress.getSize():]
        mosaic = MosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaic.getSize():]
        endHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[endHeight.getSize():]
        status = LockStatusDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[status.getSize():]
        hashAlgorithm = LockHashAlgorithmDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[hashAlgorithm.getSize():]
        secret = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[secret.getSize():]
        recipient = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[recipient.getSize():]
        return SecretLockInfoBuilder(superObject.version, ownerAddress, mosaic, endHeight, status, hashAlgorithm, secret, recipient)

    def getOwnerAddress(self) -> AddressDto:
        """Gets owner address.
        Returns:
            Owner address.
        """
        return self.ownerAddress

    def getMosaic(self) -> MosaicBuilder:
        """Gets mosaic associated with lock.
        Returns:
            Mosaic associated with lock.
        """
        return self.mosaic

    def getEndHeight(self) -> HeightDto:
        """Gets height at which the lock expires.
        Returns:
            Height at which the lock expires.
        """
        return self.endHeight

    def getStatus(self) -> LockStatusDto:
        """Gets flag indicating whether or not the lock was already used.
        Returns:
            Flag indicating whether or not the lock was already used.
        """
        return self.status

    def getHashAlgorithm(self) -> LockHashAlgorithmDto:
        """Gets hash algorithm.
        Returns:
            Hash algorithm.
        """
        return self.hashAlgorithm

    def getSecret(self) -> Hash256Dto:
        """Gets transaction secret.
        Returns:
            Transaction secret.
        """
        return self.secret

    def getRecipient(self) -> AddressDto:
        """Gets transaction recipient.
        Returns:
            Transaction recipient.
        """
        return self.recipient

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.ownerAddress.getSize()
        size += self.mosaic.getSize()
        size += self.endHeight.getSize()
        size += self.status.getSize()
        size += self.hashAlgorithm.getSize()
        size += self.secret.getSize()
        size += self.recipient.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.ownerAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaic.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.endHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.status.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.hashAlgorithm.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.secret.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.recipient.serialize())  # kind:CUSTOM
        return bytes_
