# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Manual test for controller/module discovery and messaging.

    To set up, the controller must be running mosquito:

        `sudo apt-get install mosquitto`

    Deploy this file and the device net source to the controller and
    module hardware.

    From the PiDeviceNet directory on the respective controller and module
    devices...

    Start the controller first with:

        `python3 -m pi_device_net.tests.manual_test_discovery controller`

    Then start the module with:

        `python3 -m pi_device_net.tests.manual_test_discovery module`

    They will both log some messages and the module will send ten updates
    to the controller, after which they will both exit.

    If you start the module before the controller, they should still find
    each other and connect.
"""
import json
import logging
import sys
import time

from pi_device_net.controller import ControlNetwork
from pi_device_net.module import ModuleNetwork

SYSTEM = "testing"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] "
           "[%(name)s.%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z")
LOG = logging.getLogger('test_discovery')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Need to run as either 'controller' or 'module'.")
        exit(1)

    mode = sys.argv[1]

    # We only want to process 10 messages before stopping the controller
    counter = 0

    def on_controller_message(module, topic, packet):
        global counter
        print(f"CONTROLLER: module {module!r} : "
              f"topic {topic!r} : "
              f"{json.dumps(packet, sort_keys=True)}")
        counter += 1

    def on_module_message(module, topic, packet):
        print(f"MODULE: module {module!r} : "
              f"topic {topic!r} : "
              f"{json.dumps(packet, sort_keys=True)}")

    if mode == 'controller':
        controller = ControlNetwork(SYSTEM, on_controller_message)
        while counter < 10:
            # Broadcast a discovery request (and connect to any modules
            # responding to it)
            controller.discover()

            # For every module we know about...
            modules = controller.list_modules()
            for module in modules:
                # ... send them an administration message test
                controller.publish(f"{module}/admin", 'ping')

            # Be kind to our CPU and logging output
            time.sleep(1)

    elif mode == 'module':
        module = ModuleNetwork(SYSTEM, 'module', on_module_message)

        # Block until we get and process a discovery request from
        # a controller (at least, until we give up).
        module.discover()
        for i in range(10):
            module.publish('counter', {'count': i})
            time.sleep(1)
        module.stop()

    else:
        print(f"Unsupported mode: {mode!r}; must be 'head' or 'tail'.")
        exit(1)
