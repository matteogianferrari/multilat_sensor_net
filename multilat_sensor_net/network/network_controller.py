"""This module implements the NetworkController class.

The NetworkController class is responsible for managing the distributed network composed of sensor nodes.
It integrates functionalities for handling network state, aggregating distance measurements,
and computing target positions through multilateration.

Additionally, it provides a gRPC server interface to allow external clients to interact with the network,
and query target positions.

Classes:
    NetworkController: NetworkController manages the distributed network composed of sensor nodes.

Usage Example:
    from multilat_sensor_net.network import NetworkController

    obj = NetworkController(socket_addr="localhost:50052", verbose=False)

    obj.start()
"""

from multilat_sensor_net.network import NetworkData, NetworkService, NetworkDealer
from multilat_sensor_net.estimator import Multilateration


class NetworkController:
    """NetworkController manages the distributed network composed of sensor nodes.

    This class integrates functionalities for handling the network's state, aggregating
    distance measurements, and computing the global target position. It also facilitates
    interaction with external clients through a gRPC server.

    Attributes:
        data: A NetworkData instance that encapsulates the network's state.
        dealer: A NetworkDealer for aggregating distance measurements using ZeroMQ.
        estimator: A Multilateration instance that computes the global target position.
        service: A NetworkService instance that manages the gRPC server, allowing external
            clients to interact with the network.
    """

    def __init__(self, socket_addr: str, verbose: bool = False) -> None:
        """Initializes the NetworkController.

        Args:
            socket_addr: The socket address where the gRPC server will listen (e.g., 'localhost:50052').
            verbose: Flag indicating whether the classes must produce an output.
                Defaults to False.
        """
        # Domain object
        self.data = NetworkData()

        # ZeroMQ dealer
        self.dealer = NetworkDealer(verbose=verbose)

        # Multilateration estimator
        self.estimator = Multilateration(verbose=verbose)

        # gRPC service
        self.service = NetworkService(
            data_ref=self.data,
            dealer_ref=self.dealer,
            estimator_ref=self.estimator,
            socket_addr=socket_addr,
            verbose=verbose
        )

    def start(self) -> None:
        """Starts the network controller's service.
        """
        self.service.serve()
