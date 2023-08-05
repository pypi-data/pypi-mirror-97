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
from .KeyDto import KeyDto
from .LinkActionDto import LinkActionDto

# from binascii import hexlify

class AccountKeyLinkTransactionBodyBuilder:
    """Binary layout for an account key link transaction.

    Attributes:
        linkedPublicKey: Linked public key.
        linkAction: Link action.
    """
    linkedPublicKey = bytes(32)
    linkAction = LinkActionDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountKeyLinkTransactionBodyBuilder:
        """Creates an instance of AccountKeyLinkTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountKeyLinkTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        linkedPublicKey_ = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        linkedPublicKey = linkedPublicKey_.key
        bytes_ = bytes_[linkedPublicKey_.getSize():]
        linkAction_ = LinkActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        linkAction = linkAction_.value
        bytes_ = bytes_[linkAction_.getSize():]

        # create object and call
        result = AccountKeyLinkTransactionBodyBuilder()
        result.linkedPublicKey = linkedPublicKey
        result.linkAction = linkAction
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += KeyDto(self.linkedPublicKey).getSize()
        size += LinkActionDto(self.linkAction).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, KeyDto(self.linkedPublicKey).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('linkedPublicKey', hexlify(KeyDto(self.linkedPublicKey).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, LinkActionDto(self.linkAction).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('linkAction', hexlify(LinkActionDto(self.linkAction).serialize())))
        return bytes_
