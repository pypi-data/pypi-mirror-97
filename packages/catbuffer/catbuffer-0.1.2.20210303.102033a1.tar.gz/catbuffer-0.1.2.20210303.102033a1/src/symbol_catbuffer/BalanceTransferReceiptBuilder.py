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
from .MosaicBuilder import MosaicBuilder
from .ReceiptBuilder import ReceiptBuilder
from .ReceiptTypeDto import ReceiptTypeDto

class BalanceTransferReceiptBuilder(ReceiptBuilder):
    """Binary layout for a balance transfer receipt.

    Attributes:
        mosaic: Mosaic.
        senderAddress: Mosaic sender address.
        recipientAddress: Mosaic recipient address.
    """

    def __init__(self, version: int, type: ReceiptTypeDto, mosaic: MosaicBuilder, senderAddress: AddressDto, recipientAddress: AddressDto):
        """Constructor.
        Args:
            version: Receipt version.
            type: Receipt type.
            mosaic: Mosaic.
            senderAddress: Mosaic sender address.
            recipientAddress: Mosaic recipient address.
        """
        super().__init__(version, type)
        self.mosaic = mosaic
        self.senderAddress = senderAddress
        self.recipientAddress = recipientAddress


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> BalanceTransferReceiptBuilder:
        """Creates an instance of BalanceTransferReceiptBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of BalanceTransferReceiptBuilder.
        """
        bytes_ = bytes(payload)
        superObject = ReceiptBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        mosaic = MosaicBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[mosaic.getSize():]
        senderAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[senderAddress.getSize():]
        recipientAddress = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[recipientAddress.getSize():]
        return BalanceTransferReceiptBuilder(superObject.version, superObject.type, mosaic, senderAddress, recipientAddress)

    def getMosaic(self) -> MosaicBuilder:
        """Gets mosaic.
        Returns:
            Mosaic.
        """
        return self.mosaic

    def getSenderAddress(self) -> AddressDto:
        """Gets mosaic sender address.
        Returns:
            Mosaic sender address.
        """
        return self.senderAddress

    def getRecipientAddress(self) -> AddressDto:
        """Gets mosaic recipient address.
        Returns:
            Mosaic recipient address.
        """
        return self.recipientAddress

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.mosaic.getSize()
        size += self.senderAddress.getSize()
        size += self.recipientAddress.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.mosaic.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.senderAddress.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.recipientAddress.serialize())  # kind:CUSTOM
        return bytes_
