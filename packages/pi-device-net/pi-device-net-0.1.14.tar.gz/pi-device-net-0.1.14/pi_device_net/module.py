# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    PiDeviceNet Module. Each device client should instantiate a module to
    publish the device data through, and to receive controller messages,
    and messages from other related modules
"""
import json
import logging
import socket
import struct
import time
from dataclasses import asdict
from uuid import uuid4

import paho.mqtt.client as mqtt

from pi_device_net.constants import (ModuleState, MULTICAST_GROUP,
                                     MULTICAST_PORT,
                                     DISCOVERY_PACKET_SIZE, Command,
                                     ControllerConnectReply, ModulePublish,
                                     ModuleFound)

LOG = logging.getLogger(__name__)


class ModuleNetwork():
    """ PiDeviceNet Module

    When you initialize you specify a message callback, which is how you
    will receive all messages.

    Your application must call `module.discover()` to connect to the
    Controller.
    """

    def __init__(self,
                 system_name,
                 module_name,
                 message_callback,
                 multicast_group=None,
                 multicast_port=None,
                 discovery_size=None):
        """ Initialize the Module.

        Parameters
        ----------
        system_name : String
            The name of the control network.  The controllers and all modules
            must be using the same system name.  You can run multiple isolated
            device networks on a single router if they have different system
            names.
        module_name : String
            A descriptive yet short name for this module.  Used in messaging.
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
        """
        self.id = str(uuid4())
        self.system = system_name
        self.module_name = module_name
        self.host = socket.getfqdn()
        self.root_topic = None
        self.topics = set()
        self.state = ModuleState.STOPPED
        self.multicast_group = multicast_group or MULTICAST_GROUP
        self.multicast_port = multicast_port or MULTICAST_PORT
        self.discovery_size = discovery_size or DISCOVERY_PACKET_SIZE
        self._discovery_socket = None
        self._mqtt = None
        self._message_callback = message_callback

    def discover(self, timeout=None):
        """ Wait to be discovered by a controller.

        Connects to the controller when found. The default behavior is to
        lock up forever, opening and closing the discovery socket, until
        a controller is found.  This can be refined (for testing, if nothing
        else) by specifying `timeout` and `retries`.

        Parameters
        ----------
        timeout : Float
            How long the module tries to access the discovery port before
            giving up and closing the port.  Defaults to FOREVER.
        """
        self.state = ModuleState.DISCOVERY

        start_time = time.time()
        while self.state == ModuleState.DISCOVERY:
            # Make sure we have a discovery socket
            if self._discovery_socket is None:
                self._discovery_socket = self._connect_socket()

            try:
                data, address = self._discovery_socket.recvfrom(
                    self.discovery_size)
                try:
                    # Got data! See if it parses...
                    packet = json.loads(data)
                    system = packet.get('system')

                    # We only connect to the system we are a part of
                    if system == self.system:
                        command = packet.get('command')

                        if command == Command.DISCOVER.value:
                            # Reply that we have been found
                            self._reply_found(address)

                        elif command == Command.CONNECT.value:
                            # We have been told to connect, so do that
                            connect = ControllerConnectReply(**packet)

                            # But only if they are telling US to connect
                            if connect.id == self.id:
                                LOG.info(f"Connecting to {connect.broker} "
                                         f"as {connect.topic}")
                                self._mqtt = self._connect_mqtt(connect.broker,
                                                                connect.topic)

                                # We are running now, so the discovery loop
                                # will exit
                                self.state = ModuleState.RUNNING

                        else:
                            LOG.info(f"Unsupported discovery command "
                                     f"{command!r}")
                    else:
                        LOG.info(f"Unrecognized system {system!r} "
                                 f"at {address}")

                except Exception as e:
                    LOG.error(f"Problem reading incoming packet: "
                              f"{type(e)} {e}: \n{data}")
            except BlockingIOError as e:
                pass
            except Exception as e:
                LOG.error(f"Unmanaged exception {type(e)}: {e}")

            # No need to lock the CPU
            time.sleep(1)

            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError("Timed out waiting for discovery.")

    def stop(self):
        """ Stopping the module means disconnecting any discovery
        or messaging connections and changing state.
        """
        if self.state is ModuleState.STOPPED:
            LOG.warning("Already stopped.")
        if self._mqtt is not None:
            self._mqtt.disconnect()
            self._mqtt = None
        if self._discovery_socket is not None:
            self._discovery_socket.close()
            self._discovery_socket = None
        self.state = ModuleState.STOPPED

    def publish(self, topic, message):
        """ Publish a (module-specific) message.

        Parameters
        ----------
        topic : String
            The specific topic under this system/module to publish to:
                "<system_name>/<module_name>/<topic>"
        message : Any
            Any json-parsable message
        """
        if self.state is not ModuleState.RUNNING:
            LOG.warning("Attempting to send message before running.")

        cmd = ModulePublish(system=self.system,
                            module=self.module_name,
                            id=self.id,
                            message=message)
        packet = asdict(cmd)
        topic_path = f"{self.root_topic}/{topic}"
        payload = json.dumps(packet).encode()
        LOG.debug(f"Module publish topic {topic_path!r}: {payload}")
        # QOS 1 : At least once
        self._mqtt.publish(topic_path, payload, qos=1)

    def subscribe(self, topic, module=None):
        """ Subscribe to a topic.

        The most likely use is to get information from other modules
        so that this module can coordinate with another module (e.g.
        a flow totalizer reporting flow, that a flow controller can use
        to regulate the flow).

        Parameters
        ----------
        topic : String
            Specific topic to subscribe to
        module : String
            If specified, the module we want to subscribe against.  Defaults
            to the wildcard '+' to subscribe to all modules, giving a full
            topic path of:

                `<system_name>/<module>/<topic>`
            or:
                `<system_name>/+/<topic>`
        """
        if self.state is not ModuleState.RUNNING:
            LOG.warning("Attempting to subscribe before running.")

        module = module or '+'
        topic_path = f"{self.system}/{module}/{topic}"
        LOG.debug(f"Module subscribed topic {topic_path!r}")
        self.topics.add(topic_path)
        self._mqtt.subscribe(topic_path)

    def _connect_socket(self):
        """ Connect to the discovery socket.

        Returns
        -------
        Socket
        """
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.setblocking(False)
        sock.bind(('', self.multicast_port))
        mreq = struct.pack('4sL',
                           socket.inet_aton(self.multicast_group),
                           socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP,
                        socket.IP_ADD_MEMBERSHIP,
                        mreq)
        return sock

    def _reply_found(self, address):
        """ Reply to a discovery broadcast, that we are found.

        address : (String, Int)
            Controller address as returned from the socket, as a tuple
            (<host>, <port>)
        """
        reply = ModuleFound(module=self.module_name,
                            id=self.id,
                            host=self.host)
        packet = asdict(reply)
        self._discovery_socket.sendto(json.dumps(packet).encode(), address)

    def _connect_mqtt(self, broker, topic):
        """ Connect to the messaging broker and set the topic for this
        module as set by the controller.

        Subscribes to "<topic>/admin" (which ends up being
        "<system_name>/<module>/admin") so the controller can talk directly
        to this module.

        Parameters
        ----------
        broker : String
            Broker IP address, sent as part of the Connect message
        topic : String
            Root topic in the form "<system_name>/<module>" as sent by
            the Connect message.

        Returns
        -------
        mqtt.Client
        """
        client = None
        if broker and topic:
            if self._discovery_socket is not None:
                self._discovery_socket.close()
                self._discovery_socket = None

            self.root_topic = topic
            admin_topic = f'{topic}/admin'
            self.topics.add(admin_topic)

            client = mqtt.Client(client_id=self.id)
            client.on_connect = self._connect_cb
            client.on_disconnect = self._disconnect_cb
            client.on_message = self._message_cb
            client.enable_logger()
            client.connect(broker)

            client.loop_start()
        return client

    def _connect_cb(self, client, userdata, flags, rc):
        """ MQTT callback on_connect; re-subscribes to all topics.
        """
        LOG.info("MQTT Connected")
        for topic in self.topics:
            LOG.info(f"... subscribing to {topic!r}")
            client.subscribe(topic)

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
            LOG.debug(f"Module received {packet}")
        except Exception as e:
            return

        # Only manage messages to our system
        system = packet.get('system')
        if system != self.system:
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
