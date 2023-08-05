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
from .BlockDurationDto import BlockDurationDto
from .EmbeddedTransactionBuilder import EmbeddedTransactionBuilder
from .EntityTypeDto import EntityTypeDto
from .KeyDto import KeyDto
from .MosaicDefinitionTransactionBodyBuilder import MosaicDefinitionTransactionBodyBuilder
from .MosaicFlagsDto import MosaicFlagsDto
from .MosaicIdDto import MosaicIdDto
from .MosaicNonceDto import MosaicNonceDto
from .NetworkTypeDto import NetworkTypeDto

# from binascii import hexlify

class EmbeddedMosaicDefinitionTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded mosaic definition transaction.

    Attributes:
        body: Mosaic definition transaction body.
    """
    VERSION = 1
    ENTITY_TYPE = 0x414d

    def __init__(self, signerPublicKey: KeyDto, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = MosaicDefinitionTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedMosaicDefinitionTransactionBuilder:
        """Creates an instance of EmbeddedMosaicDefinitionTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedMosaicDefinitionTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = MosaicDefinitionTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = EmbeddedMosaicDefinitionTransactionBuilder(superObject.signerPublicKey, superObject.network)
        # nothing needed to copy into EmbeddedTransaction
        result.body = body
        return result

    @property
    def id(self):
        return self.body.id

    @id.setter
    def id(self, id): # MARKER1 AttributeKind.CUSTOM
        self.body.id = id

    @property
    def duration(self):
        return self.body.duration

    @duration.setter
    def duration(self, duration): # MARKER1 AttributeKind.CUSTOM
        self.body.duration = duration

    @property
    def nonce(self):
        return self.body.nonce

    @nonce.setter
    def nonce(self, nonce): # MARKER1 AttributeKind.CUSTOM
        self.body.nonce = nonce

    @property
    def flags(self):
        return self.body.flags

    @flags.setter
    def flags(self, flags): # MARKER1 AttributeKind.FLAGS
        self.body.flags = flags

    @property
    def divisibility(self):
        return self.body.divisibility

    @divisibility.setter
    def divisibility(self, divisibility): # MARKER1 AttributeKind.SIMPLE
        self.body.divisibility = divisibility

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
        # print("8. {:20s} : ".format('mosaicDefinitionTransactionBody'))
        return bytes_
