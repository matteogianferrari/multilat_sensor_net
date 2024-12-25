"""This module implements the TargetController class.

The TargetController class serves as a facade for managing a target within a 3D space.
It integrates domain logic, gRPC services, and position updating mechanisms to control
the target's behavior based on predefined trajectories.

Classes:
    TargetController: TargetController serves as a facade for managing a target in a 3D space.

Usage Example:
    from multilat_sensor_net.target import TargetController

    obj = TargetController(
        socket_addr="localhost:50051",
        path_file="./data/path.json",
        freq=3,
        loop_path=True,
        verbose=True
    )
    obj.start()

    # After some time in the terminal press CTRL + C to terminate the process
"""

from multilat_sensor_net.target import TargetData, TargetService, TargetUpdater
import numpy as np


class TargetController:
    """TargetController serves as a facade for managing a target in a 3D space.

    This class encapsulates the creation and coordination of the TargetData, TargetService,
    and TargetUpdater classes. It provides a simplified interface to start and manage the
    target's behavior, including handling network communications and updating the
    target's position based on predefined trajectories.

    Attributes:
        domain_obj: A TargetData instance that encapsulates the target's state.
        service: A TargetService instance that manages the gRPC server, allowing external
            clients to interact with the target over the network.
        updater: A TargetUpdater instance responsible for updating the target's position
            based on trajectory waypoints loaded from a JSON file. It operates in a separate
            thread at a specified frequency.
    """

    def __init__(
            self,
            socket_addr: str,
            path_file: str,
            freq: float,
            loop_path: bool = False,
            verbose: bool = False
    ) -> None:
        """Initializes the TargetController.

        Args:
            socket_addr: The socket address where the gRPC server will listen (e.g., 'localhost:50051').
            path_file: The JSON file path containing the trajectory waypoints for the target's movement.
            freq: The update frequency in Hertz [Hz] for the position updater thread.
            loop_path: Flag indicating whether to loop the trajectory waypoints indefinitely.
                Defaults to False.
            verbose: Flag indicating whether the classes must produce an output.
                Defaults to False.
        """
        # Domain object
        self.domain_obj = TargetData(start_pos=np.array([0., 0., 0.]))

        # gRPC service
        self.service = TargetService(target_ref=self.domain_obj, socket_addr=socket_addr, verbose=verbose)

        # Position updater
        self.updater = TargetUpdater(
            target_ref=self.domain_obj,
            path_file=path_file,
            freq=freq,
            loop_path=loop_path,
            verbose=verbose
        )

    def start(self) -> None:
        """Starts the target controller's services.

        This method initiates the position updater thread and starts the gRPC server,
        enabling the target to begin moving along the predefined trajectory and accept
        external requests via gRPC.
        """
        self.updater.start()
        self.service.serve()
