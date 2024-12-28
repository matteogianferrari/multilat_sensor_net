"""This module implements the ClientApp class.

The ClientApp class is responsible for implementing the application. It communicates with the distributed
network via gRPC to retrieve the target global position, and to track and predict its state.

Classes:
    ClientApp: ClientApp class that implements the client application.

Usage Example:
    from multilat_sensor_net.client import ClientApp
    from datetime import datetime

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    obj = ClientApp(
        client_id=1,
        service_addr="localhost:50052",
        freq=3,
        output_trajectory_path=f"../data/run_{current_time}.csv",
        verbose=False
    )

    obj.run()
"""

from multilat_sensor_net.generated import network_pb2, network_pb2_grpc
from multilat_sensor_net.client import Tracker
import numpy as np
import grpc
import time


class ClientApp:
    """ClientApp class that implements the client application.

    This class implements the logic for the client application. It communicates via gRPC
    with a distributed network to manage its behavior and requests the target global position.

    Attributes:
        client_id: An integer indicating the client ID.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
        freq: A float indicating the frequency [Hz] of request for the target position.
        output_trajectory_path: A string containing the name and the path of the CSV file
            used to store the target predicted position.
        _tracker: A Tracker instance used to track the target in a 3D space.
        _channel: A gRPC channel for communicating with the distributed network service.
        _network_stub: A gRPC stub object used to call remote methods on the network service.
    """

    def __init__(
            self,
            client_id: int,
            service_addr: str,
            freq: float,
            output_trajectory_path: str,
            verbose: bool = False
    ) -> None:
        """Initializes the ClientApp.

        Args:
            client_id: The ID related to the client.
            service_addr: The gRPC service address for the distributed network.
            freq: The frequency [Hz] at which distance measurements are requested.
            output_trajectory_path: The CSV file path where to output the tracked target position.
            verbose: Flag indicating whether the classes must produce an output.
        """
        # Client attributes
        self.client_id = client_id

        # Logging attributes:
        self.verbose = verbose

        # Tracking attributes
        self.freq = freq
        self.output_trajectory_path = output_trajectory_path
        self._tracker = Tracker()

        # gRPC attributes
        self._channel = grpc.insecure_channel(service_addr)
        self._network_stub = network_pb2_grpc.NetworkStub(self._channel)

    def _start_network(self) -> bool:
        """Starts the distributed network via gRPC.

        Returns:
             True if the network was successfully started; False otherwise.
        """
        # Creates a request message
        request = network_pb2.StartRequest(client_id=self.client_id)

        # Ask the distributed network to start operating using the gRPC function
        response = self._network_stub.StartNetwork(request)

        return response.status == network_pb2.SS_OK

    def _track_target(self) -> None:
        """Tracks the target position using the tracker and the distributed network.

        The target global position is requested at the distributed network via gRPC,
        then this measurement is used in the tracker to predict and update the predicted
        target position.

        When a keyboard interrupt is identified, the function stops the distributed network.
        """
        # Create a request message
        request = network_pb2.TargetRequest(client_id=self.client_id)

        try:
            with open(self.output_trajectory_path, 'a') as file:
                # Writes the header of the csv file
                file.write("X;Y;Z\n")

                # Main loop
                while True:
                    # Asks the distributed network to send the target global position using gRPC
                    # The function call will block execution until it receives a response
                    # from the server or encounters an error (like a timeout)
                    response = self._network_stub.GetTargetGlobalPosition(request)

                    # Edge case
                    # Check if the network is not active
                    if response.status == network_pb2.TS_ERROR:
                        if self.verbose:
                            print(f"ClientApp: Cannot retrieve target position because the network is not active")

                        return

                    # Creates the measurement array from the response
                    measurement = np.array([response.x, response.y, response.z])

                    # Tracks the target
                    self._tracker.tracker_core(measurement=measurement)

                    # Gets the predicted target position
                    pred_pos = self._tracker.get_predicted_position()

                    if self.verbose:
                        print(f"ClientApp: Predicted position: {pred_pos[0]:.3f};{pred_pos[1]:.3f};{pred_pos[2]:.3f}")

                    # Appends the predicted position into the csv file
                    file.write(f"{pred_pos[0]:.3f};{pred_pos[1]:.3f};{pred_pos[2]:.3f}\n")

                    # Sleeps for an interval to match the specified frequency
                    time.sleep(1.0 / self.freq)
        except KeyboardInterrupt:
            print("ClientApp: Application stopped")

    def run(self) -> None:
        """Executes the client application.
        """
        if self._start_network():
            print("ClientApp: Network started")

            self._track_target()
        else:
            print("ClientApp: Failed to start the network")
