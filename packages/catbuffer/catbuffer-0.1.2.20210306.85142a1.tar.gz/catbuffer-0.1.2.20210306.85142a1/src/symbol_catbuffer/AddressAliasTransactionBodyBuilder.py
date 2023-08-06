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
from .AddressDto import AddressDto
from .AliasActionDto import AliasActionDto
from .NamespaceIdDto import NamespaceIdDto

def toHexString(bin):
    return hexlify(bin).decode('utf-8')

class AddressAliasTransactionBodyBuilder:
    """Binary layout for an address alias transaction.

    Attributes:
        namespaceId: Identifier of the namespace that will become an alias.
        address: Aliased address.
        aliasAction: Alias action.
    """
    namespaceId = NamespaceIdDto().namespaceId
    address = bytes(24)
    aliasAction = AliasActionDto(0).value

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AddressAliasTransactionBodyBuilder:
        """Creates an instance of AddressAliasTransactionBodyBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AddressAliasTransactionBodyBuilder.
        """
        bytes_ = bytes(payload)

        namespaceId_ = NamespaceIdDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        namespaceId = namespaceId_.namespaceId
        bytes_ = bytes_[namespaceId_.getSize():]
        address_ = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1_byte
        address = address_.address
        bytes_ = bytes_[address_.getSize():]
        aliasAction_ = AliasActionDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        aliasAction = aliasAction_.value
        bytes_ = bytes_[aliasAction_.getSize():]

        # create object and call
        result = AddressAliasTransactionBodyBuilder()
        result.namespaceId = namespaceId
        result.address = address
        result.aliasAction = aliasAction
        return result

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += NamespaceIdDto(self.namespaceId).getSize()
        size += AddressDto(self.address).getSize()
        size += AliasActionDto(self.aliasAction).getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, NamespaceIdDto(self.namespaceId).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, AddressDto(self.address).serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, AliasActionDto(self.aliasAction).serialize())  # kind:CUSTOM
        return bytes_

    def __str__(self):
        """Returns nice representation.
        Returns:
            Printable string
        """
        result = ''
        result += '{:24s} : {}\n'.format('namespaceId', toHexString(NamespaceIdDto(self.namespaceId).serialize()))
        result += '{:24s} : {}\n'.format('address', toHexString(AddressDto(self.address).serialize()))
        result += '{:24s} : {}\n'.format('aliasAction', toHexString(AliasActionDto(self.aliasAction).serialize()))
        return result
