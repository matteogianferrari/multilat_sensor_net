"""
This module implements the NetworkDealer class.

The NetworkDealer class manages communication with nodes in the distributed network using ZeroMQ.
It acts as a DEALER socket to send requests and receive responses from nodes,
allowing it to collect distance measurements asynchronously.

Classes:
    NetworkDealer: NetworkDealer class for managing the communication with distributed nodes via ZeroMQ.

Usage Example:
    from multilat_sensor_net.network import NetworkDealer
    import numpy as np

    nodes_info = {
        1: (np.array([0., 0., 0.]), "tcp://localhost:5551"),
        2: (np.array([1., 1., 0.]), "tcp://localhost:5552")
    }

    obj = NetworkDealer(verbose=False)
    obj.connect(nodes_info=nodes_info)

    distances = obj.request_distances() # Output: {1: 2.5, 2: 3.1}
"""

import zmq


class NetworkDealer:
    """NetworkDealer class for managing the communication with distributed nodes via ZeroMQ.

    This class handles communication with nodes in a distributed network using ZeroMQ DEALER socket.
    It connects to nodes, sends requests for distances, and aggregates responses asynchronously.

    Attributes:
        n_nodes: An integer indicating the number of nodes in the distributed network.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
        _socket: A ZeroMQ DEALER socket used for requesting messages.
    """

    def __init__(self, verbose: bool) -> None:
        """Initializes the NetworkDealer.

        Args:
            verbose: Flag indicating whether the classes must produce an output.
        """
        # Dealer attributes
        self.n_nodes = 0

        # Logging attributes
        self.verbose = verbose

        # ZeroMQ attributes
        self._socket = zmq.Context().socket(zmq.DEALER)

    def connect(self, nodes_info: dict) -> None:
        """Connects to the nodes in the distributed network.

        This method establishes ZeroMQ connections to the routers of each node
        in the distributed network based on the provided node information.

        Args:
            nodes_info: A dictionary containing node IDs as keys and tuples as values.
                Each tuple should include:
                - node_pos (np.array): The position of the node [x, y, z].
                - node_address (str): The ZeroMQ socket address for communication.
        """
        # Stores the number of nodes in the distributed network
        self.n_nodes = len(nodes_info)

        for node_data in nodes_info.values():
            # Creates the bind address
            bind_address = node_data[1].replace("*", "localhost")

            # Connects to the nodes routers
            self._socket.connect(bind_address)
            print(f"NetworkDealer: Connected to node on {bind_address}")

    def request_distances(self) -> dict:
        """Requests and collects distance measurements from nodes in the distributed network.

        This method sends requests to all nodes in the network, asking for their distance measurements.
        It asynchronously collects responses using ZeroMQ polling and returns the results
        as a dictionary mapping node IDs to distances.

        Returns:
            A dict where keys are node IDs (int) and values are distances (float).
        """
        # {node_id: distance}
        distances = {}

        # Sends a request to each node
        for _ in range(self.n_nodes):
            # Creates the message to send
            message = "GetDistance"
            self._socket.send_string(message)

            if self.verbose:
                print(f"NetworkDealer: Sending request {message}")

        # Uses a ZeroMQ poller to receive messages asynchronously
        poller = zmq.Poller()
        poller.register(self._socket, zmq.POLLIN)

        replies_needed = self.n_nodes
        replies_collected = 0

        # Loop for retrieving asynchronously the distances
        while replies_collected < replies_needed:
            events = dict(poller.poll(timeout=5000))  # Wait up to 5s for a reply
            if self._socket in events and events[self._socket] == zmq.POLLIN:
                # Reads the "node_id:distance" reply from the node
                reply = self._socket.recv_string()

                # Parses the message
                node_id_str, dist_str = reply.split(":")
                node_id = int(node_id_str)
                distance = float(dist_str)

                # Stores the distance in the dictionary
                distances[node_id] = distance

                replies_collected += 1
                if self.verbose:
                    print(f"NetworkDealer: Received reply from Node[{node_id_str}]: {distance:.2f}m")
            elif self.verbose:
                print("NetworkDealer: No reply yet, still waiting")

        if self.verbose:
            print("NetworkDealer: All responses collected")

        return distances
