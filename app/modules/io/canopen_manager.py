import os
import logging
from sys import platform
from canopen import Network

logger = logging.getLogger(__name__)


class CANOpenWrapper:
    def __init__(self):
        self._network_list = []

    def __del__(self):
        for network in self._network_list:
            network.disconnect()
            logger.debug(f"Network {network.channel} disconnected")

    def __len__(self):
        return len(self._network_list)

    @property
    def network_list(self):
        return self._network_list

    def init(self, channel: int = None, baud: int = None, **kwargs) -> bool:
        ret = False
        if channel is None:
            channel = 1
            logger.info(f"No CAN channel specified, default {channel=}")

        if baud is None:
            baud = 125000
            logger.info(f"No CAN baudrate specified, default {baud=}")

        try:
            if platform == "linux" or platform == "linux2":
                name = f"can{channel}"
                os.system(f'sudo ifconfig {name} down')
                os.system(f'sudo ip link set {name} type can bitrate {baud}')
                os.system(f"sudo ifconfig {name} txqueuelen {baud}")
                os.system(f'sudo ifconfig {name} up')

                network = Network()
                network = network.connect(channel=name, bustype='socketcan')

                if network is not None:
                    self._network_list.append(network)
                    logger.debug(f"Socketcan Channel {name} (baud: {baud}) successfully initialized")
                    ret = True
            else:
                logger.error("No CAN support for this platform")
                ret = False
        except Exception as e:
            logger.error(f"Error during init of canopen network: {e}")
            return False

        return ret


class CANOpenManger:
    """
    Network Manager for CANOpen and Modbus clients
    """

    def __init__(self):
        self.canopen_channels_cfg = [
            {
                "channel": 0,
                "baud": 125000
            },
            {
                "channel": 1,
                "baud": 125000
            },
            {
                "channel": 2,
                "baud": 125000
            },
            {
                "channel": 3,
                "baud": 125000
            }
        ]

        self.wrapper = CANOpenWrapper()

        logger.info("Init CANOpen io")
        for bus in self.canopen_channels_cfg:
            bus['init'] = self.wrapper.init(**bus)  # Init CAN channels

    def __len__(self):
        return len(self.wrapper)

    def __del__(self):
        del self.wrapper
        logger.debug("CANOpen Manager deleted")

    def __str__(self):
        return f"CANOpen Manager with {len(self)} channels"

    def items(self):
        return self.wrapper.network_list
