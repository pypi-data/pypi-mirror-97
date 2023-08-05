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
from. EmbeddedTransactionBuilderFactory import EmbeddedTransactionBuilderFactory
from .GeneratorUtils import GeneratorUtils
from .CosignatureBuilder import CosignatureBuilder
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .Hash256Dto import Hash256Dto

# from binascii import hexlify

class AggregateTransactionBodyBuilder:
    """Binary layout for an aggregate transaction.

    Attributes:
        transactionsHash: Aggregate hash of an aggregate's transactions.
        transactions: Sub-transaction data (transactions are variable sized and payload size is in bytes).
        cosignatures: Cosignatures data (fills remaining body space after transactions).
    """
    transactionsHash = bytes(32)
    transactions = []
    cosignatures = []

    @staticmethod
    def _loadEmbeddedTransactions(transactions, payload: bytes, payloadSize: int):
        remainingByteSizes = payloadSize
        while remainingByteSizes > 0:
            item = EmbeddedTransactionBuilderFactory.createBuilder(payload)
            transactions.append(item)
            itemSize = item.getSize() + GeneratorUtils.getTransactionPaddingSize(item.getSize(), 8)
            remainingByteSizes -= itemSize
            payload = payload[itemSize:]
        return payload

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AggregateTransactionBodyBuilder:
        """Creates an instance of AggregateTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AggregateTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        transactionsHash_ = Hash256Dto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        transactionsHash = transactionsHash_.hash256
        bytes_ = bytes_[transactionsHash_.getSize():]
        payloadSize = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIZE_FIELD
        bytes_ = bytes_[4:]
        aggregateTransactionHeader_Reserved1 = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        transactions = []
        bytes_ = AggregateTransactionBodyBuilder._loadEmbeddedTransactions(transactions, bytes_, payloadSize)
        cosignatures_ = []
        bytes_ = GeneratorUtils.loadFromBinary(CosignatureBuilder, cosignatures_, bytes_, len(bytes_))
        cosignatures = list(map(lambda e: e.as_tuple(), cosignatures_))

        # create object and call
        result = AggregateTransactionBodyBuilder()
        result.transactionsHash = transactionsHash
        result.transactions = transactions
        result.cosignatures = cosignatures
        return result

    @classmethod
    def _serialize_aligned(cls, transaction: EmbeddedTransactionBuilder) -> bytes:
        """Serializes an embeded transaction with correct padding.
        Returns:
            Serialized embedded transaction.
        """
        bytes_ = transaction.serialize()
        padding = bytes(GeneratorUtils.getTransactionPaddingSize(len(bytes_), 8))
        return GeneratorUtils.concatTypedArrays(bytes_, padding)

    @classmethod
    def _getSize_aligned(cls, transaction: EmbeddedTransactionBuilder) -> int:
        """Serializes an embeded transaction with correct padding.
        Returns:
            Serialized embedded transaction.
        """
        size = transaction.getSize()
        paddingSize = GeneratorUtils.getTransactionPaddingSize(size, 8)
        return size + paddingSize
    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += Hash256Dto(self.transactionsHash).getSize()
        size += 4  # payloadSize
        size += 4  # aggregateTransactionHeader_Reserved1
        for _ in self.transactions:
            size += self._getSize_aligned(_)
        for _ in self.cosignatures:
            size += CosignatureBuilder.from_tuple(_).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, Hash256Dto(self.transactionsHash).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('transactionsHash', hexlify(Hash256Dto(self.transactionsHash).serialize())))
        # calculate payload size
        size_value = 0
        for _ in self.transactions:
            size_value += self._getSize_aligned(_)
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(size_value, 4))  # kind:SIZE_FIELD
        # print("5. {:20s} : {}".format('payloadSize', hexlify(GeneratorUtils.uintToBuffer(size_value, 4))))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(0, 4))
        # print("1. {:20s} : {}".format('aggregateTransactionHeader_Reserved1', hexlify(GeneratorUtils.uintToBuffer(0, 4))))
        for _ in self.transactions: # kind:VAR_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self._serialize_aligned(_))
            # print("7. {:20s} : {}".format('transactions', hexlify(self._serialize_aligned(_))))
        for _ in self.cosignatures: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, CosignatureBuilder.from_tuple(_).serialize())
            # print("6. {:20s} : {}".format('cosignatures', hexlify(CosignatureBuilder.from_tuple(_).serialize())))
        return bytes_
