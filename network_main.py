if __name__ == '__main__':
    # Usage Example
    # python3 network_main.py

    from multilat_sensor_net.network import NetworkController
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Start the Network.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()

    # Create NetworkController object with the parsed arguments
    obj = NetworkController(socket_addr="localhost:50052", verbose=args.verbose)
    obj.start()
