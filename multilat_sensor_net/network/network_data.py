"""This module implements the NetworkData class.

The NetworkData class is responsible for managing the state of a distributed network.
It provides a thread-safe implementation for storing and accessing network-related data,
including active status and node information.

The class ensures fairness and avoids starvation or deadlocks by implementing
a balanced synchronization mechanism for handling concurrent read and write operations.

Classes:
    NetworkData: NetworkData class for managing a thread-safe network state.

Usage Example:
    from multilat_sensor_net.network import NetworkData
    import numpy as np

    obj = NetworkData()

    obj.add_node(node_id=1, node_pos=np.array([0., 0., 0.]), node_address="tcp://localhost:5551")

    obj.set_is_active(True)

    is_active = obj.get_is_active()  # Output: True
    nodes = obj.get_nodes_info()    # Output: {1: (array([0., 0., 0.]), 'tcp://localhost:5551')}
"""

import threading as th
import numpy as np
import copy


class NetworkData:
    """NetworkData class for managing a thread-safe network state.

    This class represents a distributed network object. This class provides methods for
    setting and retrieving the current object state and adding and retrieving nodes information.

    This class is thread-safe and provides a balanced way for readers and writers
    to call the related methods without incurring in starvation and deadlock.

    Attributes:
        _nodes: A dict containing information about connected nodes,
            including their positions and addresses {e.g., node_id: (node_pos, node_address)}.
        _is_active: A bool indicating whether the network is active or inactive.
        _synch_nodes_r: A threading semaphore used to handle requests from multiple
            reader threads for nodes methods.
        _synch_nodes_w: A threading semaphore used to handler requests from multiple
            writer threads for nodes methods.
        _mutex_nodes: A threading mutex used to lock critical sections of the code for nodes methods.
        _blocked_nodes_r: An integer count of the blocked reader threads for nodes methods.
        _blocked_nodes_w: An integer count of the blocked writer threads for nodes methods.
        _running_nodes_r: An integer count of the running reader threads for nodes methods.
        _running_nodes_w: An integer count of the running writer threads for nodes methods.
        _synch_active_r: A threading semaphore used to handle requests from multiple
            reader threads for active methods.
        _synch_active_w: A threading semaphore used to handler requests from multiple
            writer threads for active methods.
        _mutex_active: A threading mutex used to lock critical sections of the code for active methods.
        _blocked_active_r: An integer count of the blocked reader threads for active methods.
        _blocked_active_w: An integer count of the blocked writer threads for active methods.
        _running_active_r: An integer count of the running reader threads for active methods.
        _running_active_w: An integer count of the running writer threads for active methods.
    """

    def __init__(self) -> None:
        """Initializes the NetworkData.
        """
        self._nodes = dict()
        self._is_active = False

        # Threading variables
        self._synch_nodes_r = th.Semaphore()
        self._synch_nodes_w = th.Semaphore()
        self._mutex_nodes = th.Lock()

        self._blocked_nodes_r = 0
        self._blocked_nodes_w = 0
        self._running_nodes_r = 0
        self._running_nodes_w = 0

        self._synch_active_r = th.Semaphore()
        self._synch_active_w = th.Semaphore()
        self._mutex_active = th.Lock()

        self._blocked_active_r = 0
        self._blocked_active_w = 0
        self._running_active_r = 0
        self._running_active_w = 0

    def set_is_active(self, state: bool) -> None:
        """Sets the current state of the distributed network.

        Args:
            state: A bool indicating the current network state.
        """
        # Acquires the mutex for the critical section
        self._mutex_active.acquire()

        # Checks if the thread must be blocked to wait for reader or writer threads.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._running_active_r > 0 or self._running_active_w > 0:
            self._blocked_active_w += 1
        else:
            self._running_active_w += 1
            self._synch_active_w.release()

        # Releases the mutex
        self._mutex_active.release()

        # Blocks the writer thread if the previous conditional statement was True
        self._synch_active_w.acquire()

        # Sets the new state
        self._is_active = state

        # Acquires the mutex for the critical section
        self._mutex_active.acquire()

        # Decreases the number of running writers
        self._running_active_w -= 1

        # Checks if multiple reader threads or one writer thread must be unblocked.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._blocked_active_r > 0:
            # Unblocks all reader threads
            while self._blocked_active_r > 0:
                self._blocked_active_r -= 1
                self._synch_active_r.release()
        elif self._blocked_active_w > 0:
            self._blocked_active_w -= 1
            self._synch_active_w.release()

        # Releases the mutex
        self._mutex_active.release()

    def get_is_active(self) -> bool:
        """Gets the current network state.

        Returns:
            True if the distributed network is active; False otherwise.
        """
        # Acquires the mutex for the critical section
        self._mutex_active.acquire()

        # Checks if the thread must be blocked to wait for writer threads.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._running_active_w > 0 or self._blocked_active_w > 0:
            self._blocked_active_r += 1
        else:
            self._running_active_r += 1
            self._synch_active_r.release()

        # Releases the mutex
        self._mutex_active.release()

        # Blocks the reader thread if the previous conditional statement was True
        self._synch_active_r.acquire()

        # Reads the flag
        is_active = self._is_active

        # Acquires the mutex for the critical section
        self._mutex_active.acquire()

        # Decreases the number of running readers
        self._running_active_r -= 1

        # Checks if a writer thread must be unblocked.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._blocked_active_w > 0 and self._running_active_r == 0:
            self._blocked_active_w -= 1
            self._running_active_w += 1
            self._synch_active_w.release()

        # Releases the mutex
        self._mutex_active.release()

        return is_active

    def get_nodes_info(self) -> dict:
        """Gets the nodes information that are present in the distributed network.

        Returns:
            A dict containing node IDs as keys and tuples with node position
            (numpy array) and address (string) as values.
        """
        # Acquires the mutex for the critical section
        self._mutex_nodes.acquire()

        # Checks if the thread must be blocked to wait for writer threads.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._running_nodes_w > 0 or self._blocked_nodes_w > 0:
            self._blocked_nodes_r += 1
        else:
            self._running_nodes_r += 1
            self._synch_nodes_r.release()

        # Releases the mutex
        self._mutex_nodes.release()

        # Blocks the reader thread if the previous conditional statement was True
        self._synch_nodes_r.acquire()

        # Reads the target position
        nodes_info = copy.deepcopy(self._nodes)

        # Acquires the mutex for the critical section
        self._mutex_nodes.acquire()

        # Decreases the number of running readers
        self._running_nodes_r -= 1

        # Checks if a writer thread must be unblocked.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._blocked_nodes_w > 0 and self._running_nodes_r == 0:
            self._blocked_nodes_w -= 1
            self._running_nodes_w += 1
            self._synch_nodes_w.release()

        # Releases the mutex
        self._mutex_nodes.release()

        return nodes_info

    def add_node(self, node_id: int, node_pos: np.array, node_address: str) -> bool:
        """Adds a nodes to the distributed network.

        Args:
            node_id: The ID related to the node.
            node_pos: A 3D numpy array containing the sensor position [x, y, z].
            node_address: The ZeroMQ socket address for internode communication.

        Returns:
            True if the node is added to the distributed network; False otherwise.
        """
        # Acquires the mutex for the critical section
        self._mutex_nodes.acquire()

        # Checks if the thread must be blocked to wait for reader or writer threads.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._running_nodes_r > 0 or self._running_nodes_w > 0:
            self._blocked_nodes_w += 1
        else:
            self._running_nodes_w += 1
            self._synch_nodes_w.release()

        # Releases the mutex
        self._mutex_nodes.release()

        # Blocks the writer thread if the previous conditional statement was True
        self._synch_nodes_w.acquire()

        # Adds the new node
        if node_id not in self._nodes:
            self._nodes[node_id] = (node_pos, node_address)
            ret = True
        else:
            ret = False

        # Acquires the mutex for the critical section
        self._mutex_nodes.acquire()

        # Decreases the number of running writers
        self._running_nodes_w -= 1

        # Checks if multiple reader threads or one writer thread must be unblocked.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._blocked_nodes_r > 0:
            # Unblocks all reader threads
            while self._blocked_nodes_r > 0:
                self._blocked_nodes_r -= 1
                self._synch_nodes_r.release()
        elif self._blocked_nodes_w > 0:
            self._blocked_nodes_w -= 1
            self._synch_nodes_w.release()

        # Releases the mutex
        self._mutex_nodes.release()

        return ret
