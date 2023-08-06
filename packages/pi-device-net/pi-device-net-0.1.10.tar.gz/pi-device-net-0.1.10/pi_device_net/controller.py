# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    PiDeviceNet Controller.  The central hub that coordinates and receives
    messages from the various Modules.
"""
import json
import logging
import os
import socket
from dataclasses import asdict
from uuid import uuid4

import paho.mqtt.client as mqtt

from pi_device_net.constants import (
    MULTICAST_GROUP, MULTICAST_PORT, DISCOVERY_PACKET_SIZE, Command,
    ControllerPublish, ControllerDiscover, ControllerConnectReply, ModuleFound)

LOG = logging.getLogger(__name__)


class ControlNetwork():
    """ PiDeviceNet Controller

    When you initialize you specify a message callback, which is how you
    will receive all messages.

    Your application must call `controller.discover()` on a regular cycle,
    to request and process module connections.
    """

    def __init__(self,
                 system_name,
                 message_callback,
                 multicast_group=None,
                 multicast_port=None,
                 discovery_size=None,
                 testing=None):
        """ Initialize the Controller

        Parameters
        ----------
        system_name : String
            The name of the control network.  The controllers and all modules
            must be using the same system name.  You can run multiple isolated
            device networks on a single router if they have different system
            names.
        message_callback : Callable[String, String, Dict]
            For every system message received by the controller, this callable
            is called with (module_name, topic_string, message_dictionary)
        multicast_group : String
            The IP address of the multicast group used for module discovery.
            Defaults to a sensible broadcast address in `constants.py`
        multicast_port : Int
            The port that is used for the discovery socket. Defaults to the
            value in `constants.py`
        discovery_size : Int
            The size that the discovery messages are limited to.  Defaults
            to the value in `constants.py`
        testing : Bool
            If True, then skip things that are problematic during testing.
        """
        testing = testing or False

        if not testing:
            ret = os.system('systemctl status mosquitto')
            if ret != 0:
                LOG.error("The mosquitto service needs to be running")
                LOG.error("sudo apt-get install mosquitto")
                raise RuntimeError("Mosquito broker is not running.")

        self.id = str(uuid4())
        self.system = system_name
        self.host = socket.getfqdn()
        self.modules = set()
        self.multicast_group = multicast_group or MULTICAST_GROUP
        self.multicast_port = multicast_port or MULTICAST_PORT
        self.discovery_size = discovery_size or DISCOVERY_PACKET_SIZE
        self._discovery_socket = self._connect_socket()
        self._mqtt = self._connect_mqtt()
        self._message_callback = message_callback

    def discover(self):
        """ Send out a discovery request and listen for any replies.

        Call this method on a regular cycle to find and process new modules.
        May take an irregular amount of time as modules are coming online.
        """

        self._broadcast_discover()
        while True:
            try:
                # See if any modules have replied
                data, address = self._discovery_socket.recvfrom(
                    self.discovery_size)
            except BlockingIOError:
                # No messages to receive, exit discovery
                break
            except Exception as e:
                LOG.error(f"Unmanaged exception {type(e)}: {e}")
                break

            # Bogus reply, so exist discovery
            if data is None or len(data) < 1:
                break

            # We expect messages to be of a particular form, transmitted
            # as json strings.
            packet = json.loads(data)
            command = packet.get('command')
            if command == Command.FOUND.value:
                found = ModuleFound(**packet)
                module = f'{self.system}/{found.module}'
                LOG.info(f"Requesting connection to {address!r}, "
                         f"module id {found.id!r}, "
                         f"as module {module!r}")
                self._reply_connect(address, found.id, module)

    def publish(self, topic_path, message):
        """ Publish a message to a given topic.

        All modules who subscribe to this topic will receive the message.

        Parameters
        ----------
        topic_path : String
            The full topic to publish, in the format:
                "<system>/<module>/<topic>"
            where:
                system = self.system
                module = module name
                topic = specific topic
        """
        cmd = ControllerPublish(system=self.system,
                                message=message)
        packet = asdict(cmd)
        payload = json.dumps(packet).encode()
        LOG.debug(f"Controller publish to {topic_path!r}:  {payload}")
        # QOS 1 : At least once
        self._mqtt.publish(topic_path, payload, qos=1)

    def list_modules(self):
        """ List the known module topics.

        Returns
        -------
        List(String)
            The list of known modules, which are in the format:
                "<system>/<module>"
            where:
                system = self.system
                module = module name
        """
        return self.modules.copy()

    def _connect_socket(self):
        """ Connect to the discovery socket.

        Returns
        -------
        Socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        return sock

    def _connect_mqtt(self):
        """ Connect to the messaging broker

        Returns
        -------
        mqtt.Client
        """
        client = mqtt.Client(client_id=self.id)
        client.on_connect = self._connect_cb
        client.on_disconnect = self._disconnect_cb
        client.on_message = self._message_cb
        client.connect(self.host)
        client.loop_start()
        return client

    def _broadcast_discover(self):
        """ Broadcast the discovery message.
        """
        cmd = ControllerDiscover(system=self.system,
                                 host=self.host)
        packet = asdict(cmd)
        self._discovery_socket.sendto(json.dumps(packet).encode(),
                                      (self.multicast_group,
                                       self.multicast_port))

    def _reply_connect(self, address, module_id, topic):
        """ Reply to a found module with a connect message.

        Parameters
        ----------
        address : (String, Int)
            Module address as returned from the socket, as a tuple
            (<host>, <port>)
        module_id : String
            The module's unique ID as reported in the found message.
        topic : String
            The topic root we are requesting the module publish to, in
            the form "<system>/<module name>"; and to subscribe to for
            administration messages, in the form "<system>/<module name>/admin"
        """
        reply = ControllerConnectReply(system=self.system,
                                       broker=self.host,
                                       id=module_id,
                                       topic=topic)
        packet = asdict(reply)
        self._discovery_socket.sendto(json.dumps(packet).encode(), address)

        # Add the topic to our topics list and subscribe to it
        self.modules.add(topic)
        all_topics = f"{topic}/+"
        LOG.info(f"Subscribing to {all_topics!r}")
        self._mqtt.subscribe(all_topics)

    def _connect_cb(self, client, userdata, flags, rc):
        """ MQTT callback on_connect; re-subscribes to all module topics.
        """
        LOG.info("MQTT Connected")
        for module in self.modules:
            all_topics = f"{module}/+"
            LOG.info(f"... subscribing to {all_topics!r}")
            client.subscribe(all_topics)

    def _disconnect_cb(self, client, topic, flags, rc=0):
        """ MQTT callback on_disconnect
        """
        LOG.warning("MQTT Disconnected")

    def _message_cb(self, client, userdata, msg):
        """ MQTT callback on_message

        Parameters
        ----------
        msg : Any
            The message is any json-parsable entity
        """
        try:
            packet = json.loads(msg.payload)
            LOG.debug(f"Controller received {packet}")
        except Exception as e:
            LOG.error(f"Unable to package message:  {type(e)}: {e}")
            return

        # Only manage messages to our system
        system = packet.get('system')
        if system != self.system:
            return

        # Only report on Module messages
        command = packet.get('command')
        if command != Command.MODULE.value:
            return

        try:
            # This system operates on three levels for the topic:
            # System name, Module name, Topic
            _, module, topic = msg.topic.split('/')
        except Exception as e:
            LOG.error(f"Ill formatted topic {msg.topic!r};"
                      f"{type(e)}: {e}")
            return

        self._message_callback(module, topic, packet.get('message'))
