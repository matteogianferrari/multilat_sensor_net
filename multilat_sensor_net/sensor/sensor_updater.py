"""This module implements the SensorUpdater class.

The SensorUpdater class manages fetching the target's position via gRPC at a given frequency,
computing the distance from the sensor to the target by adding Uniform random noise within a
range, and updating the sensor's domain object. The measurement loop is performed in a
separate daemon thread that continues to run until the main thread finishes or a gRPC error occurs.

Classes:
    SensorUpdater: SensorUpdater class for measuring the Euclidean distance to the target.

Usage Example:
    from multi_sensor_net.sensor import SensorUpdater, SensorData
    import numpy as np
    import time

    obj = SensorData()
    updater = SensorUpdater(
        data_ref=obj,
        node_id=1,
        pos=np.array([2.0, 3.0, 4.0]),
        service_addr="localhost:50051",
        var=0.0016,
        freq=10,
        verbose=False
    )
    updater.start()

    time.sleep(5)
"""

from multilat_sensor_net.generated import target_pb2, target_pb2_grpc
import threading as th
import numpy as np
import time
import grpc


class SensorUpdater:
    """SensorUpdater class for measuring the Euclidean distance to the target.

    This class fetches the target's position via gRPC at a given frequency, computes the distance
    from the sensor to the target by adding random Uniform noise within a range, and updates
    the sensor's domain object. The measurement loop is performed in a separate daemon thread.

    Attributes:
        data_ref: A SensorData reference representing the domain logic for managing
            the sensor's position and distance to the target.
        node_id: An integer indicating the ID of the related node.
        pos: A 3D numpy array indicating the distance sensor position [x, y, z].
        freq: A float indicating the sensor measurement frequency [Hz].
        acc: A float representing the accuracy [m] used to add random Uniform noise
            to the distance measurement.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
        _channel: A gRPC channel for communicating with the target service.
        _target_stub: A gRPC stub object used to call remote methods on the target service.
        _thread: A threading daemon thread that continuously retrieves the target position and
            updates the sensor's distance measurement.
    """

    def __init__(
            self,
            data_ref,
            node_id: int,
            pos: np.array,
            service_addr: str,
            acc: float,
            freq: float,
            verbose: bool
    ) -> None:
        """Initializes the SensorUpdater.

        Args:
            data_ref: A SensorData reference for handling domain logic.
            node_id: The ID related to the node that possesses the distance sensor.
            pos: A 3D numpy array containing the position of the distance sensor.
            service_addr: The socket address (e.g., "localhost:50051") where the gRPC server is
                listening for incoming connections.
            acc: The accuracy for the random Uniform noise added to the measured distance [m].
            freq: The frequency [Hz] at which distance measurements are taken.
            verbose: Flag indicating whether the classes must produce an output.
        """
        self.data_ref = data_ref

        # Sensor attributes
        self.node_id = node_id
        self.pos = pos
        self.acc = acc
        self.freq = freq

        # gRPC stub attributes
        self._channel = grpc.insecure_channel(service_addr)
        self._target_stub = target_pb2_grpc.TargetStub(self._channel)

        # Logging attributes
        self.verbose = verbose

        # The daemon thread is used to avoid the necessity of joining it to the main thread.
        # When the main thread finished its work, the daemon thread will be automatically stopped,
        # avoiding the requirement of a stop function and signal.
        self._thread = th.Thread(target=self._run, daemon=True)

    def _compute_distance(self, target_pos: np.array) -> float:
        """Computes the distance between the sensor and the target.

        This method calculates the Euclidean distance between the sensor's position and
        the given target position, then adds Gaussian noise based on the specified variance.

        Args:
            target_pos: A 3D numpy array containing the target position.

        Returns:
            A float representing the noisy distance measurement.
        """
        # Computes the Euclidean distance between the sensor position and the target position
        distance = np.linalg.norm(self.pos - target_pos)

        # Adds gaussian noise to the distance (mean: 0, std: sqrt(var))
        distance += np.random.uniform(low=-self.acc, high=self.acc)

        return distance

    def _run(self) -> None:
        """Thread body function that continuously measures the distance to the target.

         This method runs in a separate daemon thread. It performs these steps in a loop:
             1. Requests the target's position via gRPC.
             2. Computes the distance with added random Uniform noise.
             3. Updates the sensor's domain object with the measured distance.
             4. Waits the appropriate interval to maintain the specified measurement frequency.

         The loop continues until either the main thread exits (daemon thread behavior) or
         a gRPC error occurs, in which case the loop stops.
         """
        # Computes the time interval
        interval = 1.0 / self.freq

        print(f"SensorUpdater[{self.node_id}]: Starting at {self.freq} Hz")

        # Measurement loop
        while True:
            start_time = time.time()

            # Creates a request message
            request = target_pb2.GetPositionRequest(node_id=self.node_id)

            try:
                # Gets the target position using the gRPC function
                # The function call will block execution until it receives a response
                # from the server or encounters an error (like a timeout)
                response = self._target_stub.GetPosition(request)
            except grpc.RpcError as rpc_error:
                # When the gRPC servicer is stopped the measurement thread is stopped
                print(f"SensorUpdater[{self.node_id}]: Error during gRPC communication with target")
                break

            # Computes the distance
            dist = self._compute_distance(target_pos=np.array([response.x, response.y, response.z]))

            # Updates the measured distance in the domain object
            self.data_ref.set_distance(new_distance=dist)

            # Sleeps until next interval to match the specified frequency
            elapsed = time.time() - start_time
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        print(f"SensorUpdater[{self.node_id}]: Stopped")

    def start(self) -> None:
        """Start the measurement loop in a separate thread.
        """
        self._thread.start()
