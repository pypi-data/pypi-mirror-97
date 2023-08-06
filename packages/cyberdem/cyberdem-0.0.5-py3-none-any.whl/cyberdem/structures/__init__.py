"""
CyberDEM Structures Module provides classes for CyberDEM DataTypes

CyberDEM Python

Copyright 2020 Carnegie Mellon University.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE
MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO
WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER
INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR
MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL.
CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT
TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

Released under a MIT (SEI)-style license, please see license.txt or contact
permission@sei.cmu.edu for full terms.

[DISTRIBUTION STATEMENT A] This material has been approved for public release
and unlimited distribution.  Please see Copyright notice for non-US Government
use and distribution.

DM20-0711
"""


import uuid
from cyberdem.enumerations import RelationshipType


class Relationship():
    """Represents a relationship between two CyberObjects.

    Given two CyberObjects A and B, where A administers B, the
    ``related_object_1`` would be the id of A and ``related_object_2`` would be
    the ID of B, preserving the ordering of "A administers B".

    :param related_object_1: ID of a CyberObject
    :type related_object_1: UUIDv4 string, required
    :param related_object_2: ID of a CyberObject
    :type related_object_2: UUIDv4 string, required
    :param relationship_type: value from
        :class:`~cyberdem.enumerations.RelationshipType`
    :type relationship_type: string, optional
    :param id: unique ID (UUIDv4)
    :type id: string, optional
    :param privileges: [desc]
    :type privileges: list of strings, optional

    :Example:
        >>> # Where my_application is installed on my_device
        >>> from cyberdem.base import Application, Device
        >>> from cyberdem.structures import Relationship
        >>> my_application = Application()
        >>> my_device = Device()
        >>> my_rel = Relationship(
        ...    my_device.id, my_application.id,
        ...    relationship_type='ResidesOn', privileges=['priv1', 'priv2'])
    """

    _type = "Relationship"

    def __init__(
            self, related_object_1, related_object_2, relationship_type=None,
            id=None, privileges=None):
        if id is None:
            id = str(uuid.uuid4())
        self.id = id
        self.related_object_1 = related_object_1
        self.related_object_2 = related_object_2
        if relationship_type:
            self.relationship_type = relationship_type
        if privileges:
            self.privileges = privileges

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(
                f'"{value}" is not a valid value for id. Must be a UUIDv4.')
        self._id = value

    @property
    def related_object_1(self):
        return self._related_object_1

    @related_object_1.setter
    def related_object_1(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(
                f'"{value}" is not a valid value for related_object_1. Must be'
                f' a UUIDv4 in string format')
        self._related_object_1 = value

    @property
    def related_object_2(self):
        return self._related_object_2

    @related_object_2.setter
    def related_object_2(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(
                f'"{value}" is not a valid value for related_object_2. Must be'
                f' a UUIDv4 in string format')
        self._related_object_2 = value

    @property
    def relationship_type(self):
        return self._relationship_type

    @relationship_type.setter
    def relationship_type(self, value):
        RelationshipType()._check_prop(value)
        self._relationship_type = value

    @relationship_type.deleter
    def relationship_type(self):
        del self._relationship_type

    @property
    def privileges(self):
        return self._privileges

    @privileges.setter
    def privileges(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for privileges. Must '
                f'be list of strings.')
        for v in value:
            if not isinstance(v, str):
                raise TypeError(
                    f'RelatedObject privilege list takes only string types')
        self._privileges = value

    @privileges.deleter
    def privileges(self):
        del self._privileges

    def _serialize(self):
        serialized = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                serialized[key[1:]] = value
            else:
                serialized[key] = value
            serialized['_type'] = self._type
        return serialized
