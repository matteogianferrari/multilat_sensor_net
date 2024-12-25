"""This module implements the NodeRouter class.

The NodeRouter class is responsible for managing communication between node and the distributed network using ZeroMQ.
It listens for incoming requests and responds with sensor measurements or error messages based on the request type.

Classes:
    NodeRouter: NodeRouter manages communication between node and the distributed network using ZeroMQ.

Usage Example:
    from multilat_sensor_net.sensor import SensorController
    from multilat_sensor_net.node import NodeRouter

    sensor = SensorController(node_id=1, pos=[0, 0, 0], service_addr="localhost:50051", verbose=False)
    router = NodeRouter(sensor_ref=sensor, node_id=1, bind_address="tcp://*:5551", verbose=False)

    router.start()
"""

import zmq


class NodeRouter:
    """NodeRouter manages communication between node and the distributed network using ZeroMQ.

    This class listens for incoming requests via a ZeroMQ ROUTER socket, processes those requests,
    and sends appropriate responses. It integrates with the SensorController to fetch sensor data
    and return it to the requesting node.

    Attributes:
        sensor_ref: A SensorController reference representing 
        node_id: An integer indicating the ID of the related node.
        bind_address: A string containing the binding address (e.g., "tcp://*:5551") where the ZeroMQ router will
            listen for incoming requests from the distributed network.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
        _socket: A ZeroMQ ROUTER socket used for receiving and responding to messages.
    """

    def __init__(self, sensor_ref, node_id: int, bind_address: str, verbose: bool) -> None:
        """Initializes the NodeRouter.

        Args:
            sensor_ref: A SensorController reference for handling sensor's logic.
            node_id: The ID related to the node.
            bind_address: The socket address where the ZeroMQ router will
                listen for incoming distance requests.
            verbose: Flag indicating whether the classes must produce an output.
        """
        self.sensor_ref = sensor_ref

        # Logging attributes
        self.verbose = verbose

        # Router attributes
        self.node_id = node_id
        self.bind_address = bind_address

        # ZeroMQ attributes
        self._socket = zmq.Context().socket(zmq.ROUTER)
        self._socket.bind(self.bind_address)

        print(f"NodeRouter[{self.node_id}]: Listening on {self.bind_address} for requests...")

    def start(self) -> None:
        """Starts the ZeroMQ router to handle incoming requests.

        This method continuously listens for incoming messages, processes them based on their content,
        and sends appropriate responses. Messages include requests for sensor distance or unknown commands.
        """
        while True:
            # A ROUTER socket receives frames: [identity, message]
            # Blocking function
            frames = self._socket.recv_multipart()

            # frames[0] is the identity used by DEALER, frames[1] is the actual message
            identity, request_data = frames[0], frames[1]
            msg = request_data.decode()

            if self.verbose:
                print(f"NodeRouter[{self.node_id}]: Received from distributed network request: {msg}")

            if msg == "GetDistance":
                # Reads the measurement from the sensor
                distance = self.sensor_ref.get_distance()

                # Creates the response message and sends it back to the distributed network
                reply = f"{self.node_id}:{distance}"
                self._socket.send_multipart([identity, reply.encode()])

                if self.verbose:
                    print(f"NodeRouter[{self.node_id}]: Sent distance {distance:.2f}m")
            else:
                # Sends back to the distributed network and error message
                self._socket.send_multipart([identity, "Error".encode()])

                if self.verbose:
                    print(f"NodeRouter[{self.node_id}]: Unknown request")

# TODO: stop network
