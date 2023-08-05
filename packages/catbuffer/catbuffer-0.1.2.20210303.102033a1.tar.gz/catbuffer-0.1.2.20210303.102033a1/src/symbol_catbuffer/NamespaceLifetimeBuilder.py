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
from .HeightDto import HeightDto

class NamespaceLifetimeBuilder:
    """Binary layout for namespace lifetime.

    Attributes:
        lifetimeStart: Start height.
        lifetimeEnd: End height.
    """

    def __init__(self, lifetimeStart: HeightDto, lifetimeEnd: HeightDto):
        """Constructor.
        Args:
            lifetimeStart: Start height.
            lifetimeEnd: End height.
        """
        self.lifetimeStart = lifetimeStart
        self.lifetimeEnd = lifetimeEnd


    @classmethod
    def loadFromBinary(cls, payload: bytes) -> NamespaceLifetimeBuilder:
        """Creates an instance of NamespaceLifetimeBuilder from binary payload.
        Args:
            payload: Byte payload to use to serialize the object.
        Returns:
            Instance of NamespaceLifetimeBuilder.
        """
        bytes_ = bytes(payload)

        lifetimeStart = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[lifetimeStart.getSize():]
        lifetimeEnd = HeightDto.loadFromBinary(bytes_)  # kind:CUSTOM1
        bytes_ = bytes_[lifetimeEnd.getSize():]
        return NamespaceLifetimeBuilder(lifetimeStart, lifetimeEnd)

    def getLifetimeStart(self) -> HeightDto:
        """Gets start height.
        Returns:
            Start height.
        """
        return self.lifetimeStart

    def getLifetimeEnd(self) -> HeightDto:
        """Gets end height.
        Returns:
            End height.
        """
        return self.lifetimeEnd

    def getSize(self) -> int:
        """Gets the size of the object.
        Returns:
            Size in bytes.
        """
        size = 0
        size += self.lifetimeStart.getSize()
        size += self.lifetimeEnd.getSize()
        return size

    def serialize(self) -> bytes:
        """Serializes self to bytes.
        Returns:
            Serialized bytes.
        """
        bytes_ = bytes()
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.lifetimeStart.serialize())  # kind:CUSTOM
        bytes_ = GeneratorUtils.concatTypedArrays(bytes_, self.lifetimeEnd.serialize())  # kind:CUSTOM
        return bytes_
