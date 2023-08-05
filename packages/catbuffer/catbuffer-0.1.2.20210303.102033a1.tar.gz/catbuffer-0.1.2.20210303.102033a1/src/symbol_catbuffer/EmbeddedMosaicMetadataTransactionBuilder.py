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
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .MosaicMetadataTransactionBodyBuilder import MosaicMetadataTransactionBodyBuilder
from .NetworkTypeDto import NetworkTypeDto
from .UnresolvedAddressDto import UnresolvedAddressDto
from .UnresolvedMosaicIdDto import UnresolvedMosaicIdDto

# from binascii import hexlify

class EmbeddedMosaicMetadataTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic metadata transaction.

    Attributes:
        body: Mosaic metadata transaction body.
    """
    VERSION = 1
    ENTITY_TYPE = 0x4244

    def __init__(self, signerPublicKey: KeyDto, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = MosaicMetadataTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicMetadataTransactionBuilder:
        """Creates an instance of EmbeddedMosaicMetadataTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicMetadataTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = MosaicMetadataTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = EmbeddedMosaicMetadataTransactionBuilder(superObject.signerPublicKey, superObject.network)
        # nothing needed to copy into EmbeddedTransaction
        result.body = body
        return result

    @property
    def targetAddress(self):
        return self.body.targetAddress

    @targetAddress.setter
    def targetAddress(self, targetAddress): # MARKER1 AttributeKind.CUSTOM
        self.body.targetAddress = targetAddress

    @property
    def scopedMetadataKey(self):
        return self.body.scopedMetadataKey

    @scopedMetadataKey.setter
    def scopedMetadataKey(self, scopedMetadataKey): # MARKER1 AttributeKind.SIMPLE
        self.body.scopedMetadataKey = scopedMetadataKey

    @property
    def targetMosaicId(self):
        return self.body.targetMosaicId

    @targetMosaicId.setter
    def targetMosaicId(self, targetMosaicId): # MARKER1 AttributeKind.CUSTOM
        self.body.targetMosaicId = targetMosaicId

    @property
    def valueSizeDelta(self):
        return self.body.valueSizeDelta

    @valueSizeDelta.setter
    def valueSizeDelta(self, valueSizeDelta): # MARKER1 AttributeKind.SIMPLE
        self.body.valueSizeDelta = valueSizeDelta

    @property
    def value(self):
        return self.body.value

    @value.setter
    def value(self, value): # MARKER1 AttributeKind.BUFFER
        self.body.value = value

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.body.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.body.serialize())  # kind:CUSTOM
        # print("8. {:20s} : ".format('mosaicMetadataTransactionBody'))
        return bytes_
