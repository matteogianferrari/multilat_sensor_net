"""This module implements the NodeStub class.

The NodeStub class allows nodes to register themselves to the distributed network using gRPC.

Classes:
    NodeStub: NodeStub class for handling communication between a node and the distributed network via gRPC.

Usage Example:
    from multilat_sensor_net.node import NodeStub
    import numpy as np

    obj = NodeStub(
        node_id=1,
        pos=np.array([0., 0., 0.]),
        bind_address="tcp://*:5551",
        network_service_addr="localhost:50052",
        verbose=False
    )
    obj.add_node_to_network()   # Output: True
"""

from multilat_sensor_net.generated import network_pb2, network_pb2_grpc
import numpy as np
import grpc


class NodeStub:
    """NodeStub class for handling communication between a node and the distributed network via gRPC.

    This class provides a method to interact with the distributed network, allowing nodes to
    register themselves. It manages the gRPC channel and stub required for network operations.

    Attributes:
        node_id: An integer indicating the ID of the related node.
        pos: A 3D numpy array indicating the distance sensor position [x, y, z].
        bind_address: A string containing the socket address (e.g., "tcp://*:5551") where the ZeroMQ router is
            listening for incoming distance requests.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
        _channel: A gRPC channel for communicating with the distributed network service.
        _network_stub: A gRPC stub object used to call remote methods on the network service.
    """

    def __init__(
            self,
            node_id: int,
            pos: np.array,
            bind_address: str,
            network_service_addr: str,
            verbose: bool
    ) -> None:
        """Initializes the NodeStub.

        Args:
            node_id: The ID related to the node.
            pos: A 3D numpy array containing the position of the distance sensor.
            bind_address: The socket address (e.g., "tcp://*:5551") where the ZeroMQ router is
                listening for incoming distance requests.
            network_service_addr: The socket address (e.g., "localhost:50052") where the gRPC server is
                listening for incoming connections.
            verbose: Flag indicating whether the classes must produce an output.
        """
        # Node attributes
        self.node_id = node_id
        self.pos = pos

        # Logging attributes
        self.verbose = verbose

        # ZeroMQ attributes
        self.bind_address = bind_address

        # gRPC stub attributes
        self._channel = grpc.insecure_channel(network_service_addr)
        self._network_stub = network_pb2_grpc.NetworkStub(self._channel)

    def add_node_to_network(self) -> bool:
        """Adds the node to the distributed network via gRPC.

        Constructs a message with the node's ID, bind address, and position, then sends it
        to the distributed network's gRPC service using the `AddNode` method. Handles
        any gRPC communication errors and returns the status of the operation.

        Returns:
            True if the node was successfully added to the distributed network; False otherwise.

        Raises:
            RuntimeError: If the node fails to register with the distributed network.
        """
        # Creates a request message
        request = network_pb2.NodeRequest(
            node_id=self.node_id,
            x=self.pos[0],
            y=self.pos[1],
            z=self.pos[2],
            bind_address=self.bind_address
        )

        try:
            # Adds the node to the distributed network using the gRPC function
            # The function call will block execution until it receives a response
            # from the server or encounters an error (like a timeout)
            response = self._network_stub.AddNode(request)
        except grpc.RpcError as rpc_error:
            # When the gRPC servicer is stopped the measurement thread is stopped
            print(f"NodeStub[{self.node_id}]: Error during gRPC communication with distributed network")
            return False

        if self.verbose:
            if response.status == network_pb2.NS_OK:
                print(f"NodeStub[{self.node_id}]: Added to the distributed network")
            else:
                print(f"NodeStub[{self.node_id}]: Cannot be added to the distributed network")

        return response.status == network_pb2.NS_OK
