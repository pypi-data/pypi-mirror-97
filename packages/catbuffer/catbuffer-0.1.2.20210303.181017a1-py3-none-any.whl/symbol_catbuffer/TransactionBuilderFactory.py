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

# pylint: disable=R0911,R0912

# Imports for creating transaction builders
from .TransactionBuilder import TransactionBuilder
from .AccountAddressRestrictionTransactionBuilder import AccountAddressRestrictionTransactionBuilder
from .AccountKeyLinkTransactionBuilder import AccountKeyLinkTransactionBuilder
from .AccountMetadataTransactionBuilder import AccountMetadataTransactionBuilder
from .AccountMosaicRestrictionTransactionBuilder import AccountMosaicRestrictionTransactionBuilder
from .AccountOperationRestrictionTransactionBuilder import AccountOperationRestrictionTransactionBuilder
from .AddressAliasTransactionBuilder import AddressAliasTransactionBuilder
from .AggregateBondedTransactionBuilder import AggregateBondedTransactionBuilder
from .AggregateCompleteTransactionBuilder import AggregateCompleteTransactionBuilder
from .HashLockTransactionBuilder import HashLockTransactionBuilder
from .MosaicAddressRestrictionTransactionBuilder import MosaicAddressRestrictionTransactionBuilder
from .MosaicAliasTransactionBuilder import MosaicAliasTransactionBuilder
from .MosaicDefinitionTransactionBuilder import MosaicDefinitionTransactionBuilder
from .MosaicGlobalRestrictionTransactionBuilder import MosaicGlobalRestrictionTransactionBuilder
from .MosaicMetadataTransactionBuilder import MosaicMetadataTransactionBuilder
from .MosaicSupplyChangeTransactionBuilder import MosaicSupplyChangeTransactionBuilder
from .MultisigAccountModificationTransactionBuilder import MultisigAccountModificationTransactionBuilder
from .NamespaceMetadataTransactionBuilder import NamespaceMetadataTransactionBuilder
from .NamespaceRegistrationTransactionBuilder import NamespaceRegistrationTransactionBuilder
from .NodeKeyLinkTransactionBuilder import NodeKeyLinkTransactionBuilder
from .SecretLockTransactionBuilder import SecretLockTransactionBuilder
from .SecretProofTransactionBuilder import SecretProofTransactionBuilder
from .TransferTransactionBuilder import TransferTransactionBuilder
from .VotingKeyLinkTransactionBuilder import VotingKeyLinkTransactionBuilder
from .VrfKeyLinkTransactionBuilder import VrfKeyLinkTransactionBuilder


class TransactionBuilderFactory:
    """Factory in charge of creating the specific transaction builder from the binary payload.
    """

    @classmethod
    def createBuilder(cls, payload) -> TransactionBuilder:
        """
        It creates the specific transaction builder from the payload bytes.
        Args:
            payload: bytes
        Returns:
            the TransactionBuilder subclass
        """
        headerBuilder = TransactionBuilder.loadFromBinary(payload)
        entityType = headerBuilder.type
        entityTypeVersion = headerBuilder.version
        if entityType == 0x414c and entityTypeVersion == 1:
            return AccountKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x424c and entityTypeVersion == 1:
            return NodeKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4141 and entityTypeVersion == 1:
            return AggregateCompleteTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4241 and entityTypeVersion == 1:
            return AggregateBondedTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4143 and entityTypeVersion == 1:
            return VotingKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4243 and entityTypeVersion == 1:
            return VrfKeyLinkTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4148 and entityTypeVersion == 1:
            return HashLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4152 and entityTypeVersion == 1:
            return SecretLockTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4252 and entityTypeVersion == 1:
            return SecretProofTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4144 and entityTypeVersion == 1:
            return AccountMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4244 and entityTypeVersion == 1:
            return MosaicMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4344 and entityTypeVersion == 1:
            return NamespaceMetadataTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x414d and entityTypeVersion == 1:
            return MosaicDefinitionTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x424d and entityTypeVersion == 1:
            return MosaicSupplyChangeTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4155 and entityTypeVersion == 1:
            return MultisigAccountModificationTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x424e and entityTypeVersion == 1:
            return AddressAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x434e and entityTypeVersion == 1:
            return MosaicAliasTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x414e and entityTypeVersion == 1:
            return NamespaceRegistrationTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4150 and entityTypeVersion == 1:
            return AccountAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4250 and entityTypeVersion == 1:
            return AccountMosaicRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4350 and entityTypeVersion == 1:
            return AccountOperationRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4251 and entityTypeVersion == 1:
            return MosaicAddressRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4151 and entityTypeVersion == 1:
            return MosaicGlobalRestrictionTransactionBuilder.loadFromBinary(payload)
        if entityType == 0x4154 and entityTypeVersion == 1:
            return TransferTransactionBuilder.loadFromBinary(payload)
        return headerBuilder
