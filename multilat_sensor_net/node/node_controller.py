"""This module implements the NodeController class.

The NodeController class serves as a facade for managing a distributed node and the associated distance sensor.
It integrates functionalities from the SensorController, NodeStub, and NodeRouter classes to provide
an interface for sensor management, network registration, and communication handling.

Classes:
    NodeController: NodeController serves as a facade for managing a distributed node and the related distance sensor.

Usage Example:
    from multilat_sensor_net.node import NodeController
    import numpy as np

    obj = NodeController(
        node_id=1,
        pos=np.array([0., 0., 0.]),
        bind_address="tcp://*:5551",
        target_service_addr="localhost:50051",
        network_service_addr="localhost:50052",
        verbose=False
    )
    obj.start()
"""

from multilat_sensor_net.node import NodeStub, NodeRouter
from multilat_sensor_net.sensor import SensorController
import numpy as np


class NodeController:
    """NodeController serves as a facade for managing a distributed node and the related distance sensor.

    This class encapsulates the SensorController, NodeStub, and NodeRouter classes, simplifying the management
    of sensor measurements, network registration, and internode communication. It provides an interface to
    start the sensor, register the node in the network, and read sensor data.

    Attributes:
        sensor: A SensorController instance for managing the sensor measurements and data updates.
        node_stub: A NodeStub instance for managing registration of the node in the
            distributed network via gRPC.
        node_router: A NodeRouter for managing communication of distance
            measurement requests using ZeroMQ.
    """
    def __init__(
            self,
            node_id: int,
            pos: np.array,
            bind_address: str,
            target_service_addr: str,
            network_service_addr: str,
            verbose: bool = False
    ) -> None:
        """Initializes the NodeController.

        Args:
            node_id: The ID related to the node.
            pos: A 3D numpy array containing the position of the distance sensor.
            bind_address: The ZeroMQ socket address for internode communication.
            target_service_addr: The gRPC service address for the sensor's target.
            network_service_addr: The gRPC service address for the distributed network.
            verbose: Flag indicating whether the classes must produce an output.
        """

        # Sensor object
        self.sensor = SensorController(node_id=node_id, pos=pos, service_addr=target_service_addr, verbose=verbose)

        # gRPC stub
        self.node_stub = NodeStub(
            node_id=node_id,
            pos=pos,
            bind_address=bind_address,
            network_service_addr=network_service_addr,
            verbose=verbose
        )

        # ZeroMQ router
        self.node_router = NodeRouter(
            sensor_ref=self.sensor,
            node_id=node_id,
            bind_address=bind_address,
            verbose=verbose
        )

    def start(self) -> None:
        """Starts the node's related services.

        This method starts the sensor's measurement process, registers the node in the
        distributed network, and activates the communication router if the registration is successful.
        """
        # Starts the sensor's thread
        self.sensor.start()

        # Tries to add the node to the distributed network
        # If the function return True then the ZeroMQ router is started
        if self.node_stub.add_node_to_network():
            self.node_router.start()
        else:
            return
