if __name__ == '__main__':
    # Usage Example:
    # python3 target_main.py

    from multilat_sensor_net.target import TargetController
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Start the Target.')
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose mode'
    )
    args = parser.parse_args()

    # Create TargetController object with the parsed arguments
    obj = TargetController(
        socket_addr="localhost:50051",
        path_file="data/circular_path.json",
        freq=3,
        loop_path=True,
        verbose=args.verbose  # Set verbosity based on the argument
    )

    # Start the TargetController
    obj.start()
