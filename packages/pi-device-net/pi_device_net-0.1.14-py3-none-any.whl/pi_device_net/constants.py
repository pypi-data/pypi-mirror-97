# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Useful constants and enumerations, used by PiDeviceNet
"""
from dataclasses import dataclass
from enum import Enum


class ModuleState(Enum):
    """ Module state
    """
    DISCOVERY = 'discovery'
    RUNNING = 'running'
    STOPPED = 'stopped'


class Command(Enum):
    """ Controller/Module messaging commands
    """
    DISCOVER = 'discover'
    FOUND = 'found'
    CONNECT = 'connect'
    MODULE = 'module'
    CONTROLLER = 'controller'
    ATTACH = 'attach'
    DETACH = 'detach'


# Multicast addressing:  https://tools.ietf.org/html/rfc2365
# IPv4 Organization Local Scope
# the space from which an organization should allocate sub-
# ranges when defining scopes for private use
MULTICAST_GROUP = '239.192.0.1'

# Port; arbitrary from the list of Dynamic ports
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Dynamic,_private_or_ephemeral_ports
MULTICAST_PORT = 49152

# Maximum packet size for discovery messages (just for the sockets used
# during discovery; actual connected messaging is not under an explicit limit)
DISCOVERY_PACKET_SIZE = 1024

SAMPLE_RATE = 1000

# === Various message data classes for visibility (here) and control

@dataclass
class ControllerDiscover:
    system: str
    host: str
    command: str=Command.DISCOVER.value

@dataclass
class ControllerConnectReply:
    system: str
    broker: str
    id: str
    topic: str
    command: str=Command.CONNECT.value

@dataclass
class ControllerPublish:
    system: str
    message: any
    command: str=Command.CONTROLLER.value

@dataclass
class ModuleFound:
    module: str
    id: str
    host: str
    command: str=Command.FOUND.value

@dataclass
class ModulePublish:
    system: str
    module: str
    id: str
    message: any
    command: str=Command.MODULE.value


@dataclass
class ModuleAttachMsg:
    label: str
    entry_page: str
    pages: list
    command: str = Command.ATTACH.value

@dataclass
class ModuleDetachMsg:
    command: str = Command.DETACH.value

@dataclass
class ModuleMessageMsg:
    module: str
    command: str
    data: dict
