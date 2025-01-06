
# Network Component Requirements

## 1. Functional Requirements

| Requirement ID  | Requirement Title            | Requirement Description                                                                                         |
|-----------------|------------------------------|-----------------------------------------------------------------------------------------------------------------|
| SRS-NETWORK-001 | Network Initialization       | The network must possess an unique network address.                                                             |
| SRS-NETWORK-002 | Node Management              | The network must keep track of the connected nodes, including their positions and addresses.                    |
| SRS-NETWORK-003 | Position Computation         | The network must compute the target position using multilateration based on distance measurements.              |
| SRS-NETWORK-004 | Distance Retrieval           | The network must retrieve distance measurements from nodes.                                                     |
| SRS-NETWORK-005 | Network Communication        | The network must provide a gRPC service to handle network operation requests from a client.                     |
| SRS-NETWORK-006 | Node Addition                | The network must provide a gRPC service to handle node addition requests from nodes.                            |
| SRS-NETWORK-007 | Concurrent Requests Handling | The gRPC service must handle multiple concurrent requests.                                                      |
| SRS-NETWORK-008 | Operation Status Responses   | The gRPC service must send the status of operations as responses to both clients and nodes.                     |
| SRS-NETWORK-009 | Position Reporting           | The gRPC service must send the current target global position as a response to a client when asked.             |
| SRS-NETWORK-010 | Node Count Reporting         | The gRPC service must send the number of connected nodes as a response to a client when the network is started. |

## 2. Non-Functional Requirements

| Requirement ID  | Requirement Title | Requirement Description                                                                                        |
|-----------------|-------------------|----------------------------------------------------------------------------------------------------------------|
| SRS-NETWORK-011 | Scalability       | The network must scale to handle multiple nodes without performance degradation.                               |
| SRS-NETWORK-012 | Thread-Safety     | The target must ensure fairness among threads, avoiding starvation or deadlocks.                               |
| SRS-NETWORK-013 | Fault Tolerance   | The network must handle connection failures or unexpected shutdowns gracefully.                                |
| SRS-NETWORK-014 | Usability         | Command-line arguments must allow enabling verbose logging for debugging purposes.                             |
| SRS-NETWORK-015 | Logging           | Logs must include detailed status updates for debugging, including network states and communication processes. |

## 3. Interfaces and Dependencies

### Interfaces:

- **External Interfaces:**
  - gRPC-based communication for interacting with nodes and clients.
  - ZeroMQ for asynchronous messaging with nodes for data aggregation.

### Dependencies:
- **Python Libraries:**
  - `grpc` for network communication.
  - `numpy` for mathematical operations.
  - `scipy` for numerical optimization.
  - `zmq` for ZeroMQ messaging.
  - `threading` for concurrency management.

- **Protobuf Files:**
  - Protobuf definitions in `network.proto` for gRPC service interfaces.
