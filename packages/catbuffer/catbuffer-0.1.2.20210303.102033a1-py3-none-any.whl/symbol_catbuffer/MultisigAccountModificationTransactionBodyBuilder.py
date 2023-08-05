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

# from binascii import hexlify

class MultisigAccountModificationTransactionBodyBuilder:
    """Binary layout for a multisig account modification transaction.

    Attributes:
        minRemovalDelta: Relative change of the minimal number of cosignatories required when removing an account.
        minApprovalDelta: Relative change of the minimal number of cosignatories required when approving a transaction.
        addressAdditions: Cosignatory address additions.
        addressDeletions: Cosignatory address deletions.
    """
    minRemovalDelta = int()
    minApprovalDelta = int()
    addressAdditions = []
    addressDeletions = []

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MultisigAccountModificationTransactionBodyBuilder:
        """Creates an instance of MultisigAccountModificationTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MultisigAccountModificationTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        minRemovalDelta = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]
        minApprovalDelta = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIMPLE
        bytes_ = bytes_[1:]
        addressAdditionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        addressDeletionsCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        multisigAccountModificationTransactionBody_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        addressAdditions = []  # kind:ARRAY
        for _ in range(addressAdditionsCount):
            item = UnresolvedAddressDto.loadFromBinary(bytes_)
            addressAdditions.append(item.unresolvedAddress)
            bytes_ = bytes_[item.getSize():]
        addressDeletions = []  # kind:ARRAY
        for _ in range(addressDeletionsCount):
            item = UnresolvedAddressDto.loadFromBinary(bytes_)
            addressDeletions.append(item.unresolvedAddress)
            bytes_ = bytes_[item.getSize():]

        # create object and call
        result = MultisigAccountModificationTransactionBodyBuilder()
        result.minRemovalDelta = minRemovalDelta
        result.minApprovalDelta = minApprovalDelta
        result.addressAdditions = addressAdditions
        result.addressDeletions = addressDeletions
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += 1  # minRemovalDelta
        size += 1  # minApprovalDelta
        size += 1  # addressAdditionsCount
        size += 1  # addressDeletionsCount
        size += 4  # multisigAccountModificationTransactionBody_Reserved1
        for _ in self.addressAdditions:
            size += UnresolvedAddressDto(_).getSize()
        for _ in self.addressDeletions:
            size += UnresolvedAddressDto(_).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.minRemovalDelta, 1))  # serial_kind:SIMPLE
        # print("2. {:20s} : {}".format('minRemovalDelta', hexlify(GeneratorUtils.uintToBuffer(self.minRemovalDelta, 1))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.minApprovalDelta, 1))  # serial_kind:SIMPLE
        # print("2. {:20s} : {}".format('minApprovalDelta', hexlify(GeneratorUtils.uintToBuffer(self.minApprovalDelta, 1))))
        size_value = len(self.addressAdditions)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('addressAdditionsCount', hexlify(GeneratorUtils.uintToBuffer(size_value, 1))))
        size_value = len(self.addressDeletions)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 1))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('addressDeletionsCount', hexlify(GeneratorUtils.uintToBuffer(size_value, 1))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        # print("1. {:20s} : {}".format('multisigAccountModificationTransactionBody_Reserved1', hexlify(GeneratorUtils.uintToBuffer(0, 4))))
        for _ in self.addressAdditions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(_).serialize())
            # print("6. {:20s} : {}".format('addressAdditions', hexlify(UnresolvedAddressDto(_).serialize())))
        for _ in self.addressDeletions: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedAddressDto(_).serialize())
            # print("6. {:20s} : {}".format('addressDeletions', hexlify(UnresolvedAddressDto(_).serialize())))
        return bytes_
