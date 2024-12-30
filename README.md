# MultilatSensorNet

> **Multilateration and Tracking in 3D Space Using a Distributed Network of Simulated Distance Sensors**

**MultilatSensorNet** aims to build a **distributed, scalable network of simulated distance sensors** to estimate and track an object's position in 3D space via multilateration. The system comprises four main components—**Node**, **Network**, **Target**, and **Client**—that work together to measure distances, compute multilateration with least squares, and provide real-time object tracking.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [System Components](#system-components)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

---

## Project Overview

**MultilatSensorNet** provides an environment in which:
1. A **Target** moves in 3D space following a defined trajectory.  
2. Multiple **Node** + **Sensor** pairs measure the Euclidean distance to the Target.  
3. A centralized **Network** component aggregates these distances to compute the Target’s position using multilateration with least squares.  
4. A **Client** application requests the global Target position from the Network, using a **Tracker** and **KalmanFilter** to track the movement over time.

By utilizing a distributed node-sensor approach, the system aims to be **scalable**, **robust**, and **adaptable** to various use cases.

---

## Features

- **Distributed Sensing**  
  Multiple Nodes measuring distances in 3D space, communicating results to a central Network.

- **Scalable Multilateration**  
  Use of a least squares algorithm to estimate the position of the Target from multiple distance measurements.

- **Kalman Filter Integration**  
  The Client tracks the Target in real time, smoothing measurements via a Kalman Filter.

- **Modular Architecture**  
  Each component—Node, Network, Target, and Client—can be extended or replaced, enabling flexible experimentation.

---

## System Components

1. **Node (Node + Sensor Packages)**  
   - Simulated distance sensor that measures the Euclidean distance to the Target in 3D space.  
   - Handles network requests and communications with the **Network**.

2. **Network (Network + Estimator Packages)**  
   - Central component managing Nodes registration, distance retrieval, and communication requests.  
   - Performs multilateration using least squares to compute the Target’s position.  
   - Communicates computed positions to the **Client**.

3. **Target**  
   - An object that moves in 3D space according to a defined trajectory.  
   - Provides distance information to each Node upon request.

4. **Client**  
   - Requests the global Target position from the Network.  
   - Maintains a **Tracker** with a **Kalman Filter** for smooth real-time tracking.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/matteogianferrari/multilat_sensor_net.git
   cd multilat_sensor_net
2. **Install Dependencies**
   ```bash
   pip install -r requiremets.txt

## Usage

1. **Start the Network**
    ```bash
   python3 network_main.py
2. **Start the Target Simulation** 
   ```bash
   python3 target_main.py
3. **Initialize Nodes (Minimum 3 Nodes)**
   ```bash
   python3 node_main.py --node_id 1 --pos 0 0 0
   python3 node_main.py --node_id 2 --pos 4.5 4.5 2.75
   python3 node_main.py --node_id 3 --pos 2.8 4.5 0.65
4. **Run the Client**
    ```bash
    python3 client_main.py --verbose
   
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.