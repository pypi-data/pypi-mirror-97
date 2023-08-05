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
from .GeneratorUtils import GeneratorUtils
from .ProofGammaDto import ProofGammaDto
from .ProofScalarDto import ProofScalarDto
from .ProofVerificationHashDto import ProofVerificationHashDto

class VrfProofBuilder:
    """Verfiable random function proof.

    Attributes:
        gamma: Gamma.
        verificationHash: Verification hash.
        scalar: Scalar.
    """

    def __init__(self, gamma: ProofGammaDto, verificationHash: ProofVerificationHashDto, scalar: ProofScalarDto):
        """Constructor.
        Args:
            gamma: Gamma.
            verificationHash: Verification hash.
            scalar: Scalar.
        """
        self.gamma = gamma
        self.verificationHash = verificationHash
        self.scalar = scalar


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> VrfProofBuilder:
        """Creates an instance of VrfProofBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of VrfProofBuilder.
        """
        bytes_ = bytes(payload)

        gamma = ProofGammaDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[gamma.getSize():]
        verificationHash = ProofVerificationHashDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[verificationHash.getSize():]
        scalar = ProofScalarDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[scalar.getSize():]
        return VrfProofBuilder(gamma, verificationHash, scalar)

    def getGamma(self) -> ProofGammaDto:
        """Gets gamma.
        Returns:
            Gamma.
        """
        return self.gamma

    def getVerificationHash(self) -> ProofVerificationHashDto:
        """Gets verification hash.
        Returns:
            Verification hash.
        """
        return self.verificationHash

    def getScalar(self) -> ProofScalarDto:
        """Gets scalar.
        Returns:
            Scalar.
        """
        return self.scalar

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.gamma.getSize()
        size += self.verificationHash.getSize()
        size += self.scalar.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.gamma.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.verificationHash.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.scalar.serialize())  # kind:CUSTOM
        return bytes_
