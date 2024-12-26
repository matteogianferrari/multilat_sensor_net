"""This module implements the NetworkService class.

The NetworkService class provides gRPC-based services for managing a distributed network.
It allows nodes to be added, client to start the network, and retrieve the global position of a target
using multilateration techniques.

The class integrates domain logic, communication handling, and position estimation,
ensuring smooth operation in distributed environments.

Classes:
    NetworkService: NetworkService class for handling gRPC calls related to a distributed network.

Usage Example:
    from multilat_sensor_net.target import TargetService, TargetData
    from multilat_sensor_net.estimator import Multilateration
    import numpy as np

    obj = NetworkData()
    dealer = NetworkDealer(verbose=False)
    estimator = Multilateration(verbose=False)
    service = TargetService(
        data_ref=obj,
        dealer_ref=dealer,
        estimator_ref=estimator,
        socket_addr="localhost:50052",
        verbose=False
    )
    service.serve()

    # After some time in the terminal press CTRL + C to terminate process
"""

from multilat_sensor_net.generated import dist_network_pb2_grpc, dist_network_pb2
from concurrent import futures
import numpy as np
import signal
import grpc
import sys


class NetworkService(dist_network_pb2_grpc.DistNetworkServicer):
    """NetworkService class for handling gRPC calls related to a distributed network.

    This class implements the gRPC servicer defined in the protobuf file "network.proto".
    It provides methods for serving client and nodes requests to various function
    and manages the gRPC server lifecycle.

    Attributes:
        data_ref: A NetworkData instance for managing the state and nodes of the distributed network.
        dealer_ref: A NetworkDealer instance for managing a ZeroMQ-based communication with nodes
            for collecting distance measurements.
        estimator_ref: A Multilateration instance for computing the target's global position
            using multilateration algorithms.
        socket_addr: A string containing the socket address (e.g., "localhost:50052") where the gRPC server will
            listen for incoming connections.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
    """
    
    def __init__(self, data_ref, dealer_ref, estimator_ref, socket_addr: str, verbose: bool) -> None:
        """Initializes the NetworkService.
        
        Args:
            data_ref: A NetworkData reference for managing the network state.
            dealer_ref: A NetworkDealer reference for node communication.
            estimator_ref: A Multilateration reference for estimating the target position.
            socket_addr: The socket address where the gRPC server will listen.
            verbose: Flag indicating whether the classes must produce an output.
        """
        self.data_ref = data_ref
        self.dealer_ref = dealer_ref
        self.estimator_ref = estimator_ref

        # gRPC attributes
        self.socket_addr = socket_addr

        # Logging attributes
        self.verbose = verbose

    def AddNode(self, request: dist_network_pb2.NodeRequest, context) -> dist_network_pb2.NodeResponse:
        """Handles the AddNode gRPC method.

        Args:
            request: The request message containing the node ID and the sensor position.
            context: The gRPC context for the method call.

        Returns:
            A response message containing the status of the operation.
        """
        if self.verbose:
            print(f"NetworkService: Received AddNode request from Node[{request.node_id}]")

        # Creates the numpy array
        node_pos = np.array([request.x, request.y, request.z])

        # Edge case
        # Checks if the distributed network is already active
        if self.data_ref.get_is_active():
            res = dist_network_pb2.NodeResponse(status=dist_network_pb2.NS_ERROR)
            if self.verbose:
                print(f"NetworkService: Cannot add Node[{request.node_id}] because the network is already active")

            return res

        # Adds the node to the distributed network
        ret = self.data_ref.add_node(node_id=request.node_id, node_pos=node_pos, node_address=request.bind_address)

        # Checks on result
        if ret:
            # Creates the response message
            res = dist_network_pb2.NodeResponse(status=dist_network_pb2.NS_OK)
            if self.verbose:
                print(f"NetworkService: Node[{request.node_id}] added to the network")
        else:
            res = dist_network_pb2.NodeResponse(status=dist_network_pb2.NS_ERROR)
            if self.verbose:
                print(f"NetworkService: Node[{request.node_id}] already present in the network")

        return res

    def StartNetwork(self, request: dist_network_pb2.StartRequest, context) -> dist_network_pb2.StartResponse:
        """Handles the StartNetwork gRPC method.

        Args:
            request: The request message containing the requesting client ID.
            context: The gRPC context for the method call.

        Returns:
            A response message containing the status of the operation and the
            number of nodes in the distributed network.
        """
        if self.verbose:
            print(f"NetworkService: Received StartNetwork request from Client[{request.client_id}]")

        # Edge case
        # Checks if the distributed network is already active
        if self.data_ref.get_is_active():
            res = dist_network_pb2.StartResponse(status=dist_network_pb2.SS_ERROR)
            if self.verbose:
                print(f"NetworkService: Cannot start the network because is already active")

            return res
        
        # Gets the nodes info from the domain object
        nodes_info = self.data_ref.get_nodes_info()
        n_nodes = len(nodes_info)

        # Connects the dealer to the bind addresses
        self.dealer_ref.connect(nodes_info=nodes_info)

        # Sets the sensor position in the estimator
        self.estimator_ref.set_sensor_positions(nodes_info=nodes_info)

        # Sets the network state to active
        self.data_ref.set_is_active(state=True)

        # Creates the response message
        res = dist_network_pb2.StartResponse(status=dist_network_pb2.SS_OK, n_nodes=n_nodes)

        if self.verbose:
            print(f"NetworkService: Network started successfully")

        return res

    def GetTargetGlobalPosition(
            self,
            request: dist_network_pb2.TargetRequest,
            context
    ) -> dist_network_pb2.TargetResponse:
        """Handles the GetTargetGlobalPosition gRPC method.

        Args:
            request: The request message containing the requesting client ID.
            context: The gRPC context for the method call.

        Returns:
            A response message containing the status of the operation and the
            target global position computed by the network.
        """
        if self.verbose:
            print(f"NetworkService: Received GetTargetGlobalPosition request from Client[{request.client_id}]")

        # Edge case
        # Checks if the distributed network is not active
        if not self.data_ref.get_is_active():
            res = dist_network_pb2.TargetResponse(status=dist_network_pb2.TS_ERROR, x=np.inf, y=np.inf, z=np.inf)
            if self.verbose:
                print(f"NetworkService: Cannot retrieve target global position because the network is not active")

            return res

        # Gets the distances from the sensors related to the nodes in the network
        distances = self.dealer_ref.request_distances()
        
        # Estimates the target position using multilateration
        target_pos = self.estimator_ref.estimate_position(distances=distances)

        # Creates the response message
        res = dist_network_pb2.TargetResponse(
            status=dist_network_pb2.TS_OK,
            x=target_pos[0],
            y=target_pos[1],
            z=target_pos[2]
        )

        if self.verbose:
            print(f"NetworkService: Target computed")

        return res

    def serve(self) -> None:
        """Starts the gRPC server.

        This method initializes the gRPC server, binds the NetworkService instance to the server,
        and starts listening for client requests at the specified socket address. The server
        will run indefinitely until terminated.
        """
        # Creates the grpc server
        server = grpc.server(futures.ThreadPoolExecutor())

        # Binds the NetworkService instance to the server
        dist_network_pb2_grpc.add_DistNetworkServicer_to_server(self, server)

        # Adds an insecure port to listen for requests
        server.add_insecure_port(self.socket_addr)

        # Starts the server
        server.start()

        print(f"NetworkService: gRPC servicer is running on {self.socket_addr}")

        # Define signal handler
        def handle_shutdown(signum, frame):
            print("\nNetworkService: Shutting down target gRPC server...")
            server.stop(1)
            sys.exit(0)

        # Register signal handlers
        signal.signal(signal.SIGINT, handle_shutdown)
        signal.signal(signal.SIGTERM, handle_shutdown)

        server.wait_for_termination()

# TODO: test is_active for both addnode, startnetwork, gettargetposition
# TODO: stop network (is active va disattivato)
