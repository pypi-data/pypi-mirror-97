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
from .FinalizationEpochDto import FinalizationEpochDto
from .KeyDto import KeyDto
from .LinkActionDto import LinkActionDto
from .NetworkTypeDto import NetworkTypeDto
from .VotingKeyDto import VotingKeyDto
from .VotingKeyLinkTransactionBodyBuilder import VotingKeyLinkTransactionBodyBuilder

# from binascii import hexlify

class EmbeddedVotingKeyLinkTransactionBuilder(EmbeddedTransactionBuilder):
    """Binary layout for an embedded voting key link transaction.

    Attributes:
        body: Voting key link transaction body.
    """
    VERSION = 1
    ENTITY_TYPE = 0x4143

    def __init__(self, signerPublicKey: KeyDto, network: NetworkTypeDto):
        """Constructor.
        Args:
            signerPublicKey: Entity signer's public key.
            network: Entity network.
        """
        super().__init__(signerPublicKey, self.VERSION, network, self.ENTITY_TYPE)

        self.body = VotingKeyLinkTransactionBodyBuilder()

    @classmethod
    def loadFromBinary(cls, payload: bytes) -> EmbeddedVotingKeyLinkTransactionBuilder:
        """Creates an instance of EmbeddedVotingKeyLinkTransactionBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of EmbeddedVotingKeyLinkTransactionBuilder.
        """
        bytes_ = bytes(payload)
        superObject = EmbeddedTransactionBuilder.loadFromBinary(bytes_)
        assert cls.VERSION == superObject.version, 'Invalid entity version ({})'.format(superObject.version)
        assert cls.ENTITY_TYPE == superObject.type, 'Invalid entity type ({})'.format(superObject.type)
        bytes_ = bytes_[superObject.getSize():]

        body = VotingKeyLinkTransactionBodyBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1_nonbyte
        bytes_ = bytes_[body.getSize():]

        # create object and call
        result = EmbeddedVotingKeyLinkTransactionBuilder(superObject.signerPublicKey, superObject.network)
        # nothing needed to copy into EmbeddedTransaction
        result.body = body
        return result

    @property
    def linkedPublicKey(self):
        return self.body.linkedPublicKey

    @linkedPublicKey.setter
    def linkedPublicKey(self, linkedPublicKey): # MARKER1 AttributeKind.CUSTOM
        self.body.linkedPublicKey = linkedPublicKey

    @property
    def startEpoch(self):
        return self.body.startEpoch

    @startEpoch.setter
    def startEpoch(self, startEpoch): # MARKER1 AttributeKind.CUSTOM
        self.body.startEpoch = startEpoch

    @property
    def endEpoch(self):
        return self.body.endEpoch

    @endEpoch.setter
    def endEpoch(self, endEpoch): # MARKER1 AttributeKind.CUSTOM
        self.body.endEpoch = endEpoch

    @property
    def linkAction(self):
        return self.body.linkAction

    @linkAction.setter
    def linkAction(self, linkAction): # MARKER1 AttributeKind.CUSTOM
        self.body.linkAction = linkAction

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
        # print("8. {:20s} : ".format('votingKeyLinkTransactionBody'))
        return bytes_
