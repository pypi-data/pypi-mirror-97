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
from typing import List
from .GeneratorUtils import GeneratorUtils
from .AccountKeyTypeFlagsDto import AccountKeyTypeFlagsDto
from .AccountStateFormatDto import AccountStateFormatDto
from .AccountTypeDto import AccountTypeDto
from .AddressDto import AddressDto
from .HeightActivityBucketsBuilder import HeightActivityBucketsBuilder
from .HeightDto import HeightDto
from .ImportanceSnapshotBuilder import ImportanceSnapshotBuilder
from .KeyDto import KeyDto
from .MosaicBuilder import MosaicBuilder
from .PinnedVotingKeyBuilder import PinnedVotingKeyBuilder
from .StateHeaderBuilder import StateHeaderBuilder

class AccountStateBuilder(StateHeaderBuilder):
    """Binary layout for non-historical account state.

    Attributes:
        address: Address of account.
        addressHeight: Height at which address has been obtained.
        publicKey: Public key of account.
        publicKeyHeight: Height at which public key has been obtained.
        accountType: Type of account.
        format: Account format.
        supplementalPublicKeysMask: Mask of supplemental public key flags.
        linkedPublicKey: Linked account public key.
        nodePublicKey: Node public key.
        vrfPublicKey: Vrf public key.
        votingPublicKeys: Voting public keys.
        importanceSnapshots: Current importance snapshot of the account.
        activityBuckets: Activity buckets of the account.
        balances: Balances of account.
    """

    def __init__(self, version: int, address: AddressDto, addressHeight: HeightDto, publicKey: KeyDto, publicKeyHeight: HeightDto, accountType: AccountTypeDto, format: AccountStateFormatDto, supplementalPublicKeysMask: List[AccountKeyTypeFlagsDto], linkedPublicKey: KeyDto, nodePublicKey: KeyDto, vrfPublicKey: KeyDto, votingPublicKeys: List[PinnedVotingKeyBuilder], importanceSnapshots: ImportanceSnapshotBuilder, activityBuckets: HeightActivityBucketsBuilder, balances: List[MosaicBuilder]):
        """Constructor.
        Args:
            version: Serialization version.
            address: Address of account.
            addressHeight: Height at which address has been obtained.
            publicKey: Public key of account.
            publicKeyHeight: Height at which public key has been obtained.
            accountType: Type of account.
            format: Account format.
            supplementalPublicKeysMask: Mask of supplemental public key flags.
            linkedPublicKey: Linked account public key.
            nodePublicKey: Node public key.
            vrfPublicKey: Vrf public key.
            votingPublicKeys: Voting public keys.
            importanceSnapshots: Current importance snapshot of the account.
            activityBuckets: Activity buckets of the account.
            balances: Balances of account.
        """
        super().__init__(version)
        self.address = address
        self.addressHeight = addressHeight
        self.publicKey = publicKey
        self.publicKeyHeight = publicKeyHeight
        self.accountType = accountType
        self.format = format
        self.supplementalPublicKeysMask = supplementalPublicKeysMask
        self.linkedPublicKey = linkedPublicKey
        self.nodePublicKey = nodePublicKey
        self.vrfPublicKey = vrfPublicKey
        self.votingPublicKeys = votingPublicKeys
        self.importanceSnapshots = importanceSnapshots
        self.activityBuckets = activityBuckets
        self.balances = balances


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> AccountStateBuilder:
        """Creates an instance of AccountStateBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of AccountStateBuilder.
        """
        bytes_ = bytes(payload)
        superObject = StateHeaderBuilder.loadFromBinary(bytes_)
        bytes_ = bytes_[superObject.getSize():]

        address = AddressDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[address.getSize():]
        addressHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[addressHeight.getSize():]
        publicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[publicKey.getSize():]
        publicKeyHeight = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[publicKeyHeight.getSize():]
        accountType = AccountTypeDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[accountType.getSize():]
        format = AccountStateFormatDto.loadFromBinary(bytes_)  # kind:CUSTOM2
        bytes_ = bytes_[format.getSize():]
        supplementalPublicKeysMask = AccountKeyTypeFlagsDto.bytesToFlags(bytes_, 1)  # kind:FLAGS
        bytes_ = bytes_[1:]
        votingPublicKeysCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 1))  # kind:SIZE_FIELD
        bytes_ = bytes_[1:]
        linkedPublicKey = None
        if AccountKeyTypeFlagsDto.LINKED in supplementalPublicKeysMask:
            linkedPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[linkedPublicKey.getSize():]
        nodePublicKey = None
        if AccountKeyTypeFlagsDto.NODE in supplementalPublicKeysMask:
            nodePublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[nodePublicKey.getSize():]
        vrfPublicKey = None
        if AccountKeyTypeFlagsDto.VRF in supplementalPublicKeysMask:
            vrfPublicKey = KeyDto.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[vrfPublicKey.getSize():]
        votingPublicKeys: List[PinnedVotingKeyBuilder] = []  # kind:ARRAY
        for _ in range(votingPublicKeysCount):
            item = PinnedVotingKeyBuilder.loadFromBinary(bytes_)
            votingPublicKeys.append(item)
            bytes_ = bytes_[item.getSize():]
        importanceSnapshots = None
        if format == AccountStateFormatDto.HIGH_VALUE:
            importanceSnapshots = ImportanceSnapshotBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[importanceSnapshots.getSize():]
        activityBuckets = None
        if format == AccountStateFormatDto.HIGH_VALUE:
            activityBuckets = HeightActivityBucketsBuilder.loadFromBinary(bytes_)  # kind:CUSTOM1
            bytes_ = bytes_[activityBuckets.getSize():]
        balancesCount = GeneratorUtils.bufferToUint(GeneratorUtils.getBytes(bytes_, 2))  # kind:SIZE_FIELD
        bytes_ = bytes_[2:]
        balances: List[MosaicBuilder] = []  # kind:ARRAY
        for _ in range(balancesCount):
            item = MosaicBuilder.loadFromBinary(bytes_)
            balances.append(item)
            bytes_ = bytes_[item.getSize():]
        return AccountStateBuilder(superObject.version, address, addressHeight, publicKey, publicKeyHeight, accountType, format, supplementalPublicKeysMask, linkedPublicKey, nodePublicKey, vrfPublicKey, votingPublicKeys, importanceSnapshots, activityBuckets, balances)

    def getAddress(self) -> AddressDto:
        """Gets address of account.
        Returns:
            Address of account.
        """
        return self.address

    def getAddressHeight(self) -> HeightDto:
        """Gets height at which address has been obtained.
        Returns:
            Height at which address has been obtained.
        """
        return self.addressHeight

    def getPublicKey(self) -> KeyDto:
        """Gets public key of account.
        Returns:
            Public key of account.
        """
        return self.publicKey

    def getPublicKeyHeight(self) -> HeightDto:
        """Gets height at which public key has been obtained.
        Returns:
            Height at which public key has been obtained.
        """
        return self.publicKeyHeight

    def getAccountType(self) -> AccountTypeDto:
        """Gets type of account.
        Returns:
            Type of account.
        """
        return self.accountType

    def getFormat(self) -> AccountStateFormatDto:
        """Gets account format.
        Returns:
            Account format.
        """
        return self.format

    def getSupplementalPublicKeysMask(self) -> List[AccountKeyTypeFlagsDto]:
        """Gets mask of supplemental public key flags.
        Returns:
            Mask of supplemental public key flags.
        """
        return self.supplementalPublicKeysMask

    def getLinkedPublicKey(self) -> KeyDto:
        """Gets linked account public key.
        Returns:
            Linked account public key.
        """
        if not AccountKeyTypeFlagsDto.LINKED in self.supplementalPublicKeysMask:
            raise Exception('supplementalPublicKeysMask is not set to LINKED.')
        return self.linkedPublicKey

    def getNodePublicKey(self) -> KeyDto:
        """Gets node public key.
        Returns:
            Node public key.
        """
        if not AccountKeyTypeFlagsDto.NODE in self.supplementalPublicKeysMask:
            raise Exception('supplementalPublicKeysMask is not set to NODE.')
        return self.nodePublicKey

    def getVrfPublicKey(self) -> KeyDto:
        """Gets vrf public key.
        Returns:
            Vrf public key.
        """
        if not AccountKeyTypeFlagsDto.VRF in self.supplementalPublicKeysMask:
            raise Exception('supplementalPublicKeysMask is not set to VRF.')
        return self.vrfPublicKey

    def getVotingPublicKeys(self) -> List[PinnedVotingKeyBuilder]:
        """Gets voting public keys.
        Returns:
            Voting public keys.
        """
        return self.votingPublicKeys

    def getImportanceSnapshots(self) -> ImportanceSnapshotBuilder:
        """Gets current importance snapshot of the account.
        Returns:
            Current importance snapshot of the account.
        """
        if not self.format == AccountStateFormatDto.HIGH_VALUE:
            raise Exception('format is not set to HIGH_VALUE.')
        return self.importanceSnapshots

    def getActivityBuckets(self) -> HeightActivityBucketsBuilder:
        """Gets activity buckets of the account.
        Returns:
            Activity buckets of the account.
        """
        if not self.format == AccountStateFormatDto.HIGH_VALUE:
            raise Exception('format is not set to HIGH_VALUE.')
        return self.activityBuckets

    def getBalances(self) -> List[MosaicBuilder]:
        """Gets balances of account.
        Returns:
            Balances of account.
        """
        return self.balances

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = super().getSize()
        size += self.address.getSize()
        size += self.addressHeight.getSize()
        size += self.publicKey.getSize()
        size += self.publicKeyHeight.getSize()
        size += self.accountType.getSize()
        size += self.format.getSize()
        size += 1  # supplementalPublicKeysMask
        size += 1  # votingPublicKeysCount
        if AccountKeyTypeFlagsDto.LINKED in self.supplementalPublicKeysMask:
            size += self.linkedPublicKey.getSize()
        if AccountKeyTypeFlagsDto.NODE in self.supplementalPublicKeysMask:
            size += self.nodePublicKey.getSize()
        if AccountKeyTypeFlagsDto.VRF in self.supplementalPublicKeysMask:
            size += self.vrfPublicKey.getSize()
        for _ in self.votingPublicKeys:
            size += _.getSize()
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            size += self.importanceSnapshots.getSize()
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            size += self.activityBuckets.getSize()
        size += 2  # balancesCount
        for _ in self.balances:
            size += _.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, super().serialize())
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.address.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.addressHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.publicKey.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.publicKeyHeight.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.accountType.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.format.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(AccountKeyTypeFlagsDto.flagsToInt(self.getSupplementalPublicKeysMask()), 1))  # kind:FLAGS
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getVotingPublicKeys()), 1))  # kind:SIZE_FIELD
        if AccountKeyTypeFlagsDto.LINKED in self.supplementalPublicKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.linkedPublicKey.serialize())  # kind:CUSTOM
        if AccountKeyTypeFlagsDto.NODE in self.supplementalPublicKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.nodePublicKey.serialize())  # kind:CUSTOM
        if AccountKeyTypeFlagsDto.VRF in self.supplementalPublicKeysMask:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.vrfPublicKey.serialize())  # kind:CUSTOM
        for _ in self.votingPublicKeys: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.importanceSnapshots.serialize())  # kind:CUSTOM
        if self.format == AccountStateFormatDto.HIGH_VALUE:
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.activityBuckets.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, GeneratorUtils.uintToBuffer(len(self.getBalances()), 2))  # kind:SIZE_FIELD
        for _ in self.balances: # kind:ARRAY|FILL_ARRAY
            bytes_ = GeneratorUtils.concatTypedArrays(bytes_, _.serialize())
        return bytes_
