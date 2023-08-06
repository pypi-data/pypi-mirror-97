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
from .FinalizationEpochDto import FinalizationEpochDto
from .LinkActionDto import LinkActionDto
from .VotingKeyDto import VotingKeyDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class VotingKeyLinkTransactionBodyBuilder:
    """Binary layout for a voting key link transaction.

    Attributes:
        linkedPublicKey: Linked public key.
        startEpoch: Start finalization epoch.
        endEpoch: End finalization epoch.
        linkAction: Link action.
    """
    linkedPublicKey = bytes(32)
    startEpoch = FinalizationEpochDto().finalizationEpoch
    endEpoch = FinalizationEpochDto().finalizationEpoch
    linkAction = LinkActionDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> VotingKeyLinkTransactionBodyBuilder:
        """Creates an instance of VotingKeyLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of VotingKeyLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        linkedPublicKey_ = VotingKeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        linkedPublicKey = linkedPublicKey_.votingKey
        bytes_ = bytes_[linkedPublicKey_.getSize():]
        startEpoch_ = FinalizationEpochDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        startEpoch = startEpoch_.finalizationEpoch
        bytes_ = bytes_[startEpoch_.getSize():]
        endEpoch_ = FinalizationEpochDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        endEpoch = endEpoch_.finalizationEpoch
        bytes_ = bytes_[endEpoch_.getSize():]
        linkAction_ = LinkActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        linkAction = linkAction_.value
        bytes_ = bytes_[linkAction_.getSize():]

        # create object and call
        result = VotingKeyLinkTransactionBodyBuilder()
        result.linkedPublicKey = linkedPublicKey
        result.startEpoch = startEpoch
        result.endEpoch = endEpoch
        result.linkAction = linkAction
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += VotingKeyDto(self.linkedPublicKey).getSize()
        size += FinalizationEpochDto(self.startEpoch).getSize()
        size += FinalizationEpochDto(self.endEpoch).getSize()
        size += LinkActionDto(self.linkAction).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, VotingKeyDto(self.linkedPublicKey).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, FinalizationEpochDto(self.startEpoch).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, FinalizationEpochDto(self.endEpoch).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, LinkActionDto(self.linkAction).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('linkedPublicKey', toHexString(VotingKeyDto(self.linkedPublicKey).serialize()))
        result += '{:24s} : {}\n'.format('startEpoch', toHexString(FinalizationEpochDto(self.startEpoch).serialize()))
        result += '{:24s} : {}\n'.format('endEpoch', toHexString(FinalizationEpochDto(self.endEpoch).serialize()))
        result += '{:24s} : {}\n'.format('linkAction', toHexString(LinkActionDto(self.linkAction).serialize()))
        return result
