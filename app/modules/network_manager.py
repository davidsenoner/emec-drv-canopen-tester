import os
import logging

from canopen import Network

logger = logging.getLogger(__name__)


class NetworkManager:
    def __init__(self):

        self._network_list = []

        self.channels = {
            'can0': {
                'baud': 125000,
                'bus_type': 'socketcan'
            },
            'can1': {
                'baud': 125000,
                'bus_type': 'socketcan'
            },
            'can2': {
                'baud': 125000,
                'bus_type': 'socketcan'
            },
            'can3': {
                'baud': 125000,
                'bus_type': 'socketcan'
            }
        }

        for channel in self.channels:
            try:
                baud = self.channels[channel]['baud']
                bus_type = self.channels[channel]['bus_type']

                self.init_channels(channel=channel, baud=baud)

                network = self.network_connect(channel=channel, bus_type=bus_type)
                if network is not None:
                    self.network_list.append(network)

            except Exception as e:
                logger.debug(e)

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
        try:
            return network.connect(channel=channel, bustype=bus_type)
        except Exception as e:
            logging.debug(f'Error during Network Init: {e}')
            return None
