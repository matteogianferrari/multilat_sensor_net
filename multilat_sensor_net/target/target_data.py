"""This module implements the TargetData class.

The TargetData class is used for representing an object into 3D Euclidean space.

Classes:
    TargetData: TargetData class for managing a thread-safe object in a 3D space.

Usage Example:
    import numpy as np
    from multilat_sensor_net.target import TargetData

    obj = TargetData(start_pos=np.array([0., 0., 0.]))
    obj.set_position(new_pos=np.array([1., 1., 1.]))

    obj.get_position()  # Output: array([1., 1., 1.])
"""

import threading as th
import numpy as np


class TargetData:
    """TargetData class for managing a thread-safe object in a 3D space.

    This class represents a target object that is moving in a 3D Euclidean space. This class provides methods for
    setting and retrieving the current object position.

    This class is thread-safe and provides a balanced way for readers and writers
    to call the related methods without incurring in starvation and deadlock.

    Attributes:
        _pos: A 3D numpy array indicating the current target position [x, y, z].
        _synch_r: A threading semaphore used to handle requests from multiple reader threads.
        _synch_w: A threading semaphore used to handler requests from multiple writer threads.
        _mutex: A threading mutex used to lock critical sections of the code.
        _blocked_r: An integer count of the blocked reader threads.
        _blocked_w: An integer count of the blocked writer threads.
        _running_r: An integer count of the running reader threads.
        _running_w: An integer count of the running writer threads.
    """

    def __init__(self, start_pos: np.array) -> None:
        """Initializes the TargetData.

        Args:
            start_pos: A 3D numpy array containing the starting position of the object.
        """
        # Position array
        self._pos = start_pos

        # Threading variables
        self._synch_r = th.Semaphore()
        self._synch_w = th.Semaphore()
        self._mutex = th.Lock()

        self._blocked_r = 0
        self._blocked_w = 0
        self._running_r = 0
        self._running_w = 0

    def get_position(self) -> np.array:
        """Gets the current position of the target object.

        Returns:
            A 3D numpy array indicating the current target position [x, y, z].
        """
        # Acquires the mutex for the critical section
        self._mutex.acquire()

        # Checks if the thread must be blocked to wait for writer threads.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._running_w > 0 or self._blocked_w > 0:
            self._blocked_r += 1
        else:
            self._running_r += 1
            self._synch_r.release()

        # Releases the mutex
        self._mutex.release()

        # Blocks the reader thread if the previous conditional statement was True
        self._synch_r.acquire()

        # Reads the target position
        pos = self._pos

        # Acquires the mutex for the critical section
        self._mutex.acquire()

        # Decreases the number of running readers
        self._running_r -= 1

        # Checks if a writer thread must be unblocked.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._blocked_w > 0 and self._running_r == 0:
            self._blocked_w -= 1
            self._running_w += 1
            self._synch_w.release()

        # Releases the mutex
        self._mutex.release()

        return pos

    def set_position(self, new_pos: np.array) -> None:
        """Sets the current position of the target object.

        Args:
            new_pos: A 3D numpy array indicating the current target position [x, y, z].
        """
        # Acquires the mutex for the critical section
        self._mutex.acquire()

        # Checks if the thread must be blocked to wait for reader or writer threads.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._running_r > 0 or self._running_w > 0:
            self._blocked_w += 1
        else:
            self._running_w += 1
            self._synch_w.release()

        # Releases the mutex
        self._mutex.release()

        # Blocks the writer thread if the previous conditional statement was True
        self._synch_w.acquire()

        # Sets the target position
        self._pos = new_pos

        # Acquires the mutex for the critical section
        self._mutex.acquire()

        # Decreases the number of running writers
        self._running_w -= 1

        # Checks if multiple reader threads or one writer thread must be unblocked.
        # This check ensures fairness between reader and writer threads avoiding starvation.
        if self._blocked_r > 0:
            # Unblocks all reader threads
            while self._blocked_r > 0:
                self._blocked_r -= 1
                self._synch_r.release()
        elif self._blocked_w > 0:
            self._blocked_w -= 1
            self._synch_w.release()

        # Releases the mutex
        self._mutex.release()
