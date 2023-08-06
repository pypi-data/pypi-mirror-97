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

from binascii import hexlify
from .GeneratorUtils import GeneratorUtils
from .AmountDto import AmountDto
from .MosaicSupplyChangeActionDto import MosaicSupplyChangeActionDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class MosaicSupplyChangeTransactionBodyBuilder:
    """Binary layout for a mosaic supply change transaction.

    Attributes:
        mosaicId: Affected mosaic identifier.
        delta: Change amount.
        action: Supply change action.
    """
    mosaicId = UnresolvedMosaicIdDto().unresolvedMosaicId
    delta = AmountDto().amount
    action = MosaicSupplyChangeActionDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicSupplyChangeTransactionBodyBuilder:
        """Creates an instance of MosaicSupplyChangeTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicSupplyChangeTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        mosaicId_ = UnresolvedMosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        mosaicId = mosaicId_.unresolvedMosaicId
        bytes_ = bytes_[mosaicId_.getSize():]
        delta_ = AmountDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        delta = delta_.amount
        bytes_ = bytes_[delta_.getSize():]
        action_ = MosaicSupplyChangeActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        action = action_.value
        bytes_ = bytes_[action_.getSize():]

        # create object and call
        result = MosaicSupplyChangeTransactionBodyBuilder()
        result.mosaicId = mosaicId
        result.delta = delta
        result.action = action
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += UnresolvedMosaicIdDto(self.mosaicId).getSize()
        size += AmountDto(self.delta).getSize()
        size += MosaicSupplyChangeActionDto(self.action).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, UnresolvedMosaicIdDto(self.mosaicId).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, AmountDto(self.delta).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, MosaicSupplyChangeActionDto(self.action).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('mosaicId', toHexString(UnresolvedMosaicIdDto(self.mosaicId).serialize()))
        result += '{:24s} : {}\n'.format('delta', toHexString(AmountDto(self.delta).serialize()))
        result += '{:24s} : {}\n'.format('action', toHexString(MosaicSupplyChangeActionDto(self.action).serialize()))
        return result
