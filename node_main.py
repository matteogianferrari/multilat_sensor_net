if __name__ == '__main__':
    # Usage Example
    # python3 node_main.py --node_id 3 --pos 2.8 4.5 0.65

    from multilat_sensor_net.node import NodeController
    import numpy as np
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Start the Node.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('--node_id', type=int, required=True, help='Node ID')
    parser.add_argument('--pos', type=float, nargs=3, required=True, help='Position as [x, y, z]')
    args = parser.parse_args()

    # Create NodeController object with the parsed arguments
    obj = NodeController(
        node_id=args.node_id,
        pos=np.array(args.pos),
        bind_address=f"tcp://*:555{args.node_id}",
        target_service_addr="localhost:50051",
        network_service_addr="localhost:50052",
        verbose=args.verbose
    )

    # Start the NodeController
    obj.start()
