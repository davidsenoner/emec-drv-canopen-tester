import os
import logging

from canopen import Network

logger = logging.getLogger(__name__)


class NetworkManager:
    def __init__(self):

        self._network_list = []
        baud = 125000  # baudrate

        # scan for max 16 channel and stop searching at first exception
        for channel_id in range(16):
            name = f"can{channel_id}"

            try:
                self.init_channels(channel=name, baud=baud)

                network = self.network_connect(channel=name, bus_type='socketcan')
                if network is not None:
                    self.network_list.append(network)
                    logger.debug(f"Socketcan Channel {name} (baud: {baud}) found and added to list")

            except Exception as e:
                break

    @property
    def network_list(self) -> list:
        return self._network_list

    @staticmethod
    def init_channels(channel, baud):
        os.system(f'sudo ifconfig {channel} down')
        os.system(f'sudo ip link set {channel} type can bitrate {baud}')
        os.system(f"sudo ifconfig {channel} txqueuelen {baud}")
        os.system(f'sudo ifconfig {channel} up')

    @staticmethod
    def network_connect(channel: str, bus_type: str):
        network = Network()

        return network.connect(channel=channel, bustype=bus_type)
