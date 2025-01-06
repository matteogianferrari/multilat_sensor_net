# Target Component Requirements

## 1. Functional Requirements

| Requirement ID | Requirement Title     | Requirement Description                                                                                          |
|----------------|-----------------------|------------------------------------------------------------------------------------------------------------------|
| SRS-TARGET-001 | Target Initialization | The target must possess an unique network address.                                                               |
| SRS-TARGET-002 | Trajectory Management | The target must load a predefined trajectory from a JSON file containing waypoints with x, y, and z coordinates. |
| SRS-TARGET-003 | Trajectory Management | The target must support looping the trajectory indefinitely if specified.                                        |
| SRS-TARGET-004 | Trajectory Management | The trajectory must be updated at a configurable frequency in Hertz (Hz).                                        |
| SRS-TARGET-005 | Position Updates      | The target must update its position based on trajectory waypoints.                                               |
| SRS-TARGET-006 | Network Communication | The target must provide a gRPC service to handle position requests from nodes.                                   |
| SRS-TARGET-007 | Network Communication | The gRPC service must handle multiple concurrent requests.                                                       |
| SRS-TARGET-008 | Network Communication | The gRPC service must send the current target position as a response to nodes.                                   |

## 2. Non-Functional Requirements

| Requirement ID | Requirement Title | Requirement Description                                                                                     |
|----------------|-------------------|-------------------------------------------------------------------------------------------------------------|
| SRS-TARGET-009 | Scalability       | The target must support scalable addition of requesting nodes without performance degradation.              |
| SRS-TARGET-010 | Thread-Safety     | The target must ensure fairness among threads, avoiding starvation or deadlocks.                            |
| SRS-TARGET-011 | Fault Tolerance   | The target must handle invalid or missing waypoints in the trajectory file gracefully, throwing exceptions. |
| SRS-TARGET-012 | Fault Tolerance   | The gRPC service must handle sudden shutdowns and terminate safely.                                         |
| SRS-TARGET-013 | Usability         | Command-line arguments must support enabling verbose logging for debugging purposes.                        |
| SRS-TARGET-014 | Usability         | Logs must provide detailed status updates for debugging, including position updates and server status.      |

## 3. Interfaces and Dependencies

### Interfaces:

- **External Interfaces:**
  - gRPC-based communication for target position queries.
  - JSON file input for defining trajectories.

### Dependencies:
- **Python Libraries:**
  - `numpy` for mathematical operations.
  - `grpc` for network communication.
  - `threading` for thread management.
  - `concurrent.futures` for thread management.
- **Data Files:**
  - JSON files containing trajectory waypoints.
- **Protobuf Files:**
  - Protobuf definitions in `target.proto` for gRPC service interface.
