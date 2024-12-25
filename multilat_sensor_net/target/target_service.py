"""This module implements the TargetService class.

The TargetService class is responsible for handling gRPC requests related to the position
of a target object in a 3D space. It leverages a TargetData instance to manage the underlying
domain logic for the target's position and provides a gRPC server to handle client requests.

Classes:
    TargetService: TargetService class for handling gRPC calls related to target object.

Usage Example:
    import numpy as np
    from multilat_sensor_net.target import TargetService, TargetData

    obj = TargetData(start_pos=np.array([0., 0., 0.]))
    service = TargetService(data_ref=obj, socket_addr="localhost:50051", verbose=False)
    service.serve()

    # After some time in the terminal press CTRL + C to terminate process
"""

from multilat_sensor_net.generated import target_pb2, target_pb2_grpc
from concurrent import futures
import grpc
import sys
import signal


class TargetService(target_pb2_grpc.TargetServicer):
    """TargetService class for handling gRPC calls related to target object.

    This class implements the gRPC servicer defined in the protobuf file "target.proto".
    It provides methods for serving client requests to get the position of a target
    and manages the gRPC server lifecycle.

    Attributes:
        data_ref: A TargetData reference representing the domain logic for managing
            the target's position in a 3D space.
        socket_addr: A string containing the socket address (e.g., "localhost:50051") where the gRPC server will
            listen for incoming connections.
        verbose: A boolean flag that enables logging for debugging purposes. If True, detailed
            logs about actions performed by the components will be printed to the console.
    """

    def __init__(self, data_ref, socket_addr: str, verbose: bool) -> None:
        """Initializes the TargetService.

        Args:
            data_ref: A TargetData reference for handling domain logic.
            socket_addr: The socket address where the gRPC server will listen.
            verbose: Flag indicating whether the classes must produce an output.
        """
        self.data_ref = data_ref
        self.socket_addr = socket_addr

        # Logging attributes
        self.verbose = verbose

    def GetPosition(self, request: target_pb2.GetPositionRequest, context) -> target_pb2.GetPositionResponse:
        """Handles the GetPosition gRPC method.

        Args:
            request: The request message containing the node ID.
            context: The gRPC context for the method call.

        Returns:
            A response message containing the status and the position [x, y, z] of the target.
        """
        if self.verbose:
            print(f"TargetService: Received GetPosition request from Sensor[{request.node_id}]")

        # Retrieves the current target position from the domain object
        pos = self.data_ref.get_position()

        # Creates the response message
        res = target_pb2.GetPositionResponse(
            status=target_pb2.PS_OK,
            x=pos[0],
            y=pos[1],
            z=pos[2]
        )

        return res

    def serve(self) -> None:
        """Starts the gRPC server.

        This method initializes the gRPC server, binds the TargetService instance to the server,
        and starts listening for client requests at the specified socket address. The server
        will run indefinitely until terminated.
        """
        # Creates the grpc server
        server = grpc.server(futures.ThreadPoolExecutor())

        # Binds the TargetService instance to the server
        target_pb2_grpc.add_TargetServicer_to_server(self, server)

        # Adds an insecure port to listen for requests
        server.add_insecure_port(self.socket_addr)

        # Starts the server
        server.start()

        print(f"TargetService: gRPC servicer is running on {self.socket_addr}")

        # Define signal handler
        def handle_shutdown(signum, frame):
            print("\nTargetService: Shutting down gRPC servicer...")
            server.stop(1)
            sys.exit(0)

        # Register signal handlers
        signal.signal(signal.SIGINT, handle_shutdown)
        signal.signal(signal.SIGTERM, handle_shutdown)

        # Blocks the thread until server termination
        server.wait_for_termination()
