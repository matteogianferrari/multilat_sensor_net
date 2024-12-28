if __name__ == '__main__':
    # Usage Example
    # python3 client_main.py --verbose

    from multilat_sensor_net.client import ClientApp
    from datetime import datetime
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Start the Client Application.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()

    # Format the current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # For low-speed objects use 10-20Hz
    # For high-speed objects use 20-30Hz
    obj = ClientApp(
        client_id=1,
        service_addr="localhost:50052",
        freq=15,
        output_trajectory_path=f"data/run_{current_time}.csv",
        verbose=args.verbose
    )

    obj.run()
