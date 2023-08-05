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
from .AliasActionDto import AliasActionDto
from .MosaicIdDto import MosaicIdDto
from .NamespaceIdDto import NamespaceIdDto

# from binascii import hexlify

class MosaicAliasTransactionBodyBuilder:
    """Binary layout for an mosaic alias transaction.

    Attributes:
        namespaceId: Identifier of the namespace that will become an alias.
        mosaicId: Aliased mosaic identifier.
        aliasAction: Alias action.
    """
    namespaceId = NamespaceIdDto().namespaceId
    mosaicId = MosaicIdDto().mosaicId
    aliasAction = AliasActionDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> MosaicAliasTransactionBodyBuilder:
        """Creates an instance of MosaicAliasTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of MosaicAliasTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        namespaceId_ = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        namespaceId = namespaceId_.namespaceId
        bytes_ = bytes_[namespaceId_.getSize():]
        mosaicId_ = MosaicIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        mosaicId = mosaicId_.mosaicId
        bytes_ = bytes_[mosaicId_.getSize():]
        aliasAction_ = AliasActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        aliasAction = aliasAction_.value
        bytes_ = bytes_[aliasAction_.getSize():]

        # create object and call
        result = MosaicAliasTransactionBodyBuilder()
        result.namespaceId = namespaceId
        result.mosaicId = mosaicId
        result.aliasAction = aliasAction
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += NamespaceIdDto(self.namespaceId).getSize()
        size += MosaicIdDto(self.mosaicId).getSize()
        size += AliasActionDto(self.aliasAction).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceIdDto(self.namespaceId).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('namespaceId', hexlify(NamespaceIdDto(self.namespaceId).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, MosaicIdDto(self.mosaicId).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('mosaicId', hexlify(MosaicIdDto(self.mosaicId).serialize())))
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, AliasActionDto(self.aliasAction).serialize())  # kind:CUSTOM
        # print("8. {:20s} : {}".format('aliasAction', hexlify(AliasActionDto(self.aliasAction).serialize())))
        return bytes_
