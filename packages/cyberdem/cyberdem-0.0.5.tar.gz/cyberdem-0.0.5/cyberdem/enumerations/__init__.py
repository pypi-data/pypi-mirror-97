'''
CyberDEM Enumerations Module

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
'''


class _CyberDEMEnumeration():
    """Super class for all CyberDEM enumerations"""

    _opts = []

    def _check_prop(self, value):
        """Checks to see if ``value`` is an allowed enumeration value.

        Campares the given value to the allowed options for the current
        enumeration subclass.

        :param value: user-provided value for the enumeration type
        :type value: required

        :raises ValueError: if the ``value`` is not in the allowed options of
            the enumeration class.
        """

        if value.lower() not in [o.lower() for o in self._opts]:
            raise ValueError(
                f'"{value}" is not an acceptable {self.__class__.__name__}. '
                f'Options are {", ".join(self._opts)}.')
        if value not in self._opts:
            print(
                f'Warning: "{value}" is not the same capitalization as '
                f'{self.__class__.__name__} option.')


class CyberEventPhaseType(_CyberDEMEnumeration):
    """CyberDEM CyberEventPhaseType enumeration

    :options: 'Continue', 'ContinueWithChanges', 'End', 'Start', 'Suspend'
    """

    _opts = [
        'Continue',
        'ContinueWithChanges',
        'End',
        'Start',
        'Suspend'
    ]


class DataLinkProtocolType(_CyberDEMEnumeration):
    """CyberDEM DataLinkProtocolType enumeration

    :options: 'ATM', 'Bluetooth', 'Ethernet', 'LocalTalk', 'PPP', 'TokenRing',
        'VLAN', 'WiFi', '1553Bus'
    """

    _opts = [
        'ATM',
        'Bluetooth',
        'Ethernet',
        'LocalTalk',
        'PPP',
        'TokenRing',
        'VLAN',
        'WiFi',
        '1553Bus'
    ]


class DataStatus(_CyberDEMEnumeration):
    """CyberDEM DataStatus enumeration

    :options: 'Corrupted', 'Erased', 'Manipulated', 'NonDecryptable',
        'Uncompromised'
    """

    _opts = [
        'Corrupted',
        'Erased',
        'Manipulated',
        'NonDecryptable',
        'Uncompromised'
    ]


class DataType(_CyberDEMEnumeration):
    """CyberDEM DataType enumeration

    :options: 'Code', 'Credentials', 'File'
    """

    _opts = [
        'Code',
        'Credentials',
        'File'
    ]


class DeviceType(_CyberDEMEnumeration):
    """CyberDEM DeviceType enumeration

    :options: 'Communications', 'ComputerNode', 'Controller', 'Generic', 'HMI',
        'IoT', 'Monitoring', 'Networking', 'PortableComputer', 'Printer',
        'Scanner', 'Sensor', 'StorageDevice'
    """

    _opts = [
        'Communications',
        'ComputerNode',
        'Controller',
        'Generic',
        'HMI',
        'IoT',
        'Monitoring',
        'Networking',
        'PortableComputer',
        'Printer',
        'Scanner',
        'Sensor',
        'StorageDevice'
    ]

    def _check_prop(self, value):
        """Checks to see if ``value`` is an allowed enumeration value.

        Overrides the :func:`~_CyberDEMEnumeration._check_prop` function from
        the super :class:`_CyberDEMEnumeration`

        Campares the given value to the allowed options for the current
        enumeration class (sub-class to :class:`_CyberDEMEnumeration`).

        :param value: user-provided value for the enumeration type
        :type value: list, required

        :raises ValueError: if the values in ``value`` are not in the allowed
            options.
        """
        if not isinstance(value, list):
            raise ValueError(f'"device_types" should be a list of DeviceTypes')
        for t in value:
            if t.lower() not in [o.lower() for o in self._opts]:
                raise ValueError(f'"{t}" is not a valid value for DeviceType')
            if t not in self._opts:
                print(
                    f'Warning: "{t}" is not the same capitalization as '
                    f'{self.__class__.__name__} option.')


class EncryptionType(_CyberDEMEnumeration):
    """CyberDEM EncryptionType enumeration

    :options: 'AES', 'DES', 'RSA', 'SHA', 'TripleDES', 'TwoFish'
    """

    _opts = [
        'AES',
        'DES',
        'RSA',
        'SHA',
        'TripleDES',
        'TwoFish'
    ]


class HardwareDamageType(_CyberDEMEnumeration):
    """CyberDEM HardwareDamageType enumeration

    :options: 'BootLoop', 'HardDriveErased', 'PhysicalDestruction',
    """

    _opts = [
        'BootLoop',
        'HardDriveErased',
        'PhysicalDestruction'
    ]


class HardwareDegradeType(_CyberDEMEnumeration):
    """CyberDEM HardwareDegradeType enumeration

    :options: 'BlueScreen', 'Display', 'Keyboard', 'Mouse', 'RandomText',
        'Reboot', 'Sound'
    """

    _opts = [
        'BlueScreen',
        'Display',
        'Keyboard',
        'Mouse',
        'RandomText',
        'Reboot',
        'Sound'
    ]


class LoadRateType(_CyberDEMEnumeration):
    """CyberDEM LoadRateType enumeration

    :options: 'Download', 'Upload'
    """

    _opts = [
        'Download',
        'Upload'
    ]


class MessageType(_CyberDEMEnumeration):
    """CyberDEM MessageType enumeration

    :options: 'Chat', 'Email', 'SocialMedia', 'Text'
    """

    _opts = [
        'Chat',
        'Email',
        'SocialMedia',
        'Text'
    ]


class NetworkProtocolType(_CyberDEMEnumeration):
    """CyberDEM NetworkProtocolType enumeration

    :options: 'ARP', 'ICMP', 'InternetProtocol', 'IPsec', 'NAT', 'OSPF', 'RIP'
    """

    _opts = [
        'ARP',
        'ICMP',
        'InternetProtocol',
        'IPsec',
        'NAT',
        'OSPF',
        'RIP'
    ]


class OperatingSystemType(_CyberDEMEnumeration):
    """CyberDEM OperatingSystemType enumeration

    :options: 'Android', 'AppleiOS', 'AppleMacOS', 'BellLabsUnix', 'BSDUnix',
        'CiscoIOS', 'DECHP_UX', 'DECVMS', 'Firmware', 'GNUUnix', 'IBMOS_2',
        'LinuxRedHat', 'MicrosoftDOS', 'MicrosoftWindows', 'OpenSolaris',
        'Ubuntu'
    """

    _opts = [
        'Android',
        'AppleiOS',
        'AppleMacOS',
        'BellLabsUnix',
        'BSDUnix',
        'CiscoIOS',
        'DECHP_UX',
        'DECVMS',
        'Firmware',
        'GNUUnix',
        'IBMOS_2',
        'LinuxRedHat',
        'MicrosoftDOS',
        'MicrosoftWindows',
        'OpenSolaris',
        'Ubuntu'
    ]


class PacketManipulationType(_CyberDEMEnumeration):
    """CyberDEM PacketManipulationType enumeration

    :options: 'Corruption', 'Dropped', 'Duplication', 'Redordering'
    """

    _opts = [
        'Corruption',
        'Dropped',
        'Duplication',
        'Redordering'
    ]


class PhysicalLayerType(_CyberDEMEnumeration):
    """CyberDEM PhysicalLayerType enumeration

    :options: 'Wired', 'Wireless'
    """

    _opts = [
        'Wired',
        'Wireless'
    ]


class ReconType(_CyberDEMEnumeration):
    """CyberDEM ReconType enumeration

    :options: 'AccountEnumeration', 'ARPScan', 'DeviceEnumeration',
        'DNSEnumeration', 'DomainEnumeration', 'LDAPScan', 'NetBiosScan',
        'NetworkMap', 'NTPEnumeration', 'OSScan', 'Ping', 'PingScan',
        'PortScan', 'PortSweep', 'ServiceEnumeration', 'SMTPEnumeration',
        'SNMPSweep', 'TraceRoute', 'UNIX-LinuxEnumeration',
        'VulnerabilityEnumeration', 'WindowsEnumeration'
    """

    _opts = [
        'AccountEnumeration',
        'ARPScan',
        'DeviceEnumeration',
        'DNSEnumeration',
        'DomainEnumeration',
        'LDAPScan',
        'NetBiosScan',
        'NetworkMap',
        'NTPEnumeration',
        'OSScan',
        'Ping',
        'PingScan',
        'PortScan',
        'PortSweep',
        'ServiceEnumeration',
        'SMTPEnumeration',
        'SNMPSweep',
        'TraceRoute',
        'UNIX-LinuxEnumeration',
        'VulnerabilityEnumeration',
        'WindowsEnumeration'
    ]


class RelationshipType(_CyberDEMEnumeration):
    """CyberDEM RelationshipType enumeration

    :options: 'Administers', 'ComponentOf', 'ContainedIn', 'ProvidedBy',
        'ResidesOn'
    """

    _opts = [
        'Administers',
        'ComponentOf',
        'ContainedIn',
        'ProvidedBy',
        'ResidesOn'
    ]


class SensitivityType(_CyberDEMEnumeration):
    """CyberDEM SensitivityType enumeration

    :options: 'Confidential', 'CosmicTopSecret', 'FOUO', 'FVEY', 'GDPR',
        'HIPPA', 'NATOConfidential', 'NATORestricted', 'NATOSecret', 'PII',
        'Proprietary', 'Public', 'Secret', 'SecretNoForn', 'TS', 'TS_SCI',
        'Unclassified'
    """

    _opts = [
        'Confidential',
        'CosmicTopSecret',
        'FOUO',
        'FVEY',
        'GDPR',
        'HIPPA',
        'NATOConfidential',
        'NATORestricted',
        'NATOSecret',
        'PII',
        'Proprietary',
        'Public',
        'Secret',
        'SecretNoForn',
        'TS',
        'TS_SCI',
        'Unclassified'
    ]


class ServiceType(_CyberDEMEnumeration):
    """CyberDEM ServiceType enumeration

    :options: 'ChatServer', 'DatabaseServer', 'DomainNameServer',
        'EmailServer', 'FileShare', 'Forum', 'SocialMediaServer', 'WebService'
    """

    _opts = [
        'ChatServer',
        'DatabaseServer',
        'DomainNameServer',
        'EmailServer',
        'FileShare',
        'Forum',
        'SocialMediaServer',
        'WebService'
    ]


class SystemType(_CyberDEMEnumeration):
    """CyberDEM SystemType enumeration

    :options: 'C2', 'Generic', 'ICS', 'SCADA'
    """

    _opts = [
        'C2',
        'Generic',
        'ICS',
        'SCADA'
    ]
