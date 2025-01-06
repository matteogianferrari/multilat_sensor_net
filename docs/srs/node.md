
# Node Component Requirements

## 1. Functional Requirements

| Req.ID       | Req. Cat               | Req. Description                                                                               |
|--------------|------------------------|------------------------------------------------------------------------------------------------|
| SRS-NODE-001 | Node Initialization    | The node must possess an unique ID.                                                            |
| SRS-NODE-002 | Node Initialization    | The node must possess a position in a 3D space.                                                |
| SRS-NODE-003 | Node Initialization    | The node must possess an unique network addresses.                                             |
| SRS-NODE-004 | Sensor Integration     | The node must include a sensor to measure distances to the target in 3D space.                 |
| SRS-NODE-005 | Distance Computation   | The sensor must compute Euclidean distances.                                                   |
| SRS-NODE-006 | Measurement Accuracy   | The sensor must have configurable accuracy for its measurements.                               |
| SRS-NONE-007 | Measurement Frequency  | The sensor must have configurable update frequency.                                            |
| SRS-NODE-008 | Network Registration   | The node must register itself with the distributed network via gRPC.                           |
| SRS-NODE-009 | Communication Handling | The node must handle incoming requests from the distributed network for distance measurements. |

## 2. Non-Functional Requirements

| Req.ID       | Req. Cat      | Req. Description                                                                     |
|--------------|---------------|--------------------------------------------------------------------------------------|
| SRS-NODE-010 | Scalability   | The node must support scalability to operate as part of a large distributed network. |
| SRS-NODE-011 | Thread-Safety | The node must ensure fairness among threads, avoiding starvation or deadlocks.     |
| SRS-NODE-012 | Usability     | Command-line arguments must allow enabling verbose logging for debugging purposes.   |
| SRS-NODE-013 | Logging       | Logs must include details of measurements, communications, and errors for debugging. |

## 3. Interfaces and Dependencies

### Interfaces:

- **External Interfaces:**
  - gRPC-based communication for interacting with the distributed network.
  - ZeroMQ for asynchronous messaging with the distributed network for data aggregation.

### Dependencies:

- **Python Libraries:**
  - `grpc` for network communication.
  - `numpy` for mathematical computations.
  - `zmq` for ZeroMQ messaging.
  - `threading` for concurrency management.

- **External Files:**
  - Protobuf definitions in `network.proto` for gRPC stub interfaces.
  - Protobuf definitions in `target.proto` for gRPC stub interface.
