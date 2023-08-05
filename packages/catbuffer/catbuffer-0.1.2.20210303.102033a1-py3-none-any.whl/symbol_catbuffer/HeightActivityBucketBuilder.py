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
from .AmountDto import AmountDto
from .ImportanceHeightDto import ImportanceHeightDto

class HeightActivityBucketBuilder:
    """Account activity bucket.

    Attributes:
        startHeight: Activity start height.
        totalFeesPaid: Total fees paid by account.
        beneficiaryCount: Number of times account has been used as a beneficiary.
        rawScore: Raw importance score.
    """

    def __init__(self, startHeight: ImportanceHeightDto, totalFeesPaid: AmountDto, beneficiaryCount: int, rawScore: int):
        """Constructor.
        Args:
            startHeight: Activity start height.
            totalFeesPaid: Total fees paid by account.
            beneficiaryCount: Number of times account has been used as a beneficiary.
            rawScore: Raw importance score.
        """
        self.startHeight = startHeight
        self.totalFeesPaid = totalFeesPaid
        self.beneficiaryCount = beneficiaryCount
        self.rawScore = rawScore


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> HeightActivityBucketBuilder:
        """Creates an instance of HeightActivityBucketBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of HeightActivityBucketBuilder.
        """
        bytes_ = bytes(payload)

        startHeight = ImportanceHeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[startHeight.getSize():]
        totalFeesPaid = AmountDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[totalFeesPaid.getSize():]
        beneficiaryCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 4))  # kind:SIMPLE
        bytes_ = bytes_[4:]
        rawScore = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 8))  # kind:SIMPLE
        bytes_ = bytes_[8:]
        return HeightActivityBucketBuilder(startHeight, totalFeesPaid, beneficiaryCount, rawScore)

    def getStartHeight(self) -> ImportanceHeightDto:
        """Gets activity start height.
        Returns:
            Activity start height.
        """
        return self.startHeight

    def getTotalFeesPaid(self) -> AmountDto:
        """Gets total fees paid by account.
        Returns:
            Total fees paid by account.
        """
        return self.totalFeesPaid

    def getBeneficiaryCount(self) -> int:
        """Gets number of times account has been used as a beneficiary.
        Returns:
            Number of times account has been used as a beneficiary.
        """
        return self.beneficiaryCount

    def getRawScore(self) -> int:
        """Gets raw importance score.
        Returns:
            Raw importance score.
        """
        return self.rawScore

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.startHeight.getSize()
        size += self.totalFeesPaid.getSize()
        size += 4  # beneficiaryCount
        size += 8  # rawScore
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.startHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.totalFeesPaid.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getBeneficiaryCount(), 4))  # kind:SIMPLE
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(self.getRawScore(), 8))  # kind:SIMPLE
        return bytes_
