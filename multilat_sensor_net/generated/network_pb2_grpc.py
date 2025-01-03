# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import network_pb2 as network__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in network_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class NetworkStub(object):
    """*
    Service defining the operations available for the distributed network.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddNode = channel.unary_unary(
                '/network.Network/AddNode',
                request_serializer=network__pb2.NodeRequest.SerializeToString,
                response_deserializer=network__pb2.NodeResponse.FromString,
                _registered_method=True)
        self.StartNetwork = channel.unary_unary(
                '/network.Network/StartNetwork',
                request_serializer=network__pb2.StartRequest.SerializeToString,
                response_deserializer=network__pb2.StartResponse.FromString,
                _registered_method=True)
        self.GetTargetGlobalPosition = channel.unary_unary(
                '/network.Network/GetTargetGlobalPosition',
                request_serializer=network__pb2.TargetRequest.SerializeToString,
                response_deserializer=network__pb2.TargetResponse.FromString,
                _registered_method=True)


class NetworkServicer(object):
    """*
    Service defining the operations available for the distributed network.
    """

    def AddNode(self, request, context):
        """RPC method to add a node to the distributed network.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartNetwork(self, request, context):
        """RPC method to start the distributed network.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTargetGlobalPosition(self, request, context):
        """RPC method for requesting the global position of the target in a 3D space.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NetworkServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddNode': grpc.unary_unary_rpc_method_handler(
                    servicer.AddNode,
                    request_deserializer=network__pb2.NodeRequest.FromString,
                    response_serializer=network__pb2.NodeResponse.SerializeToString,
            ),
            'StartNetwork': grpc.unary_unary_rpc_method_handler(
                    servicer.StartNetwork,
                    request_deserializer=network__pb2.StartRequest.FromString,
                    response_serializer=network__pb2.StartResponse.SerializeToString,
            ),
            'GetTargetGlobalPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTargetGlobalPosition,
                    request_deserializer=network__pb2.TargetRequest.FromString,
                    response_serializer=network__pb2.TargetResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'network.Network', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('network.Network', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Network(object):
    """*
    Service defining the operations available for the distributed network.
    """

    @staticmethod
    def AddNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/network.Network/AddNode',
            network__pb2.NodeRequest.SerializeToString,
            network__pb2.NodeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StartNetwork(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/network.Network/StartNetwork',
            network__pb2.StartRequest.SerializeToString,
            network__pb2.StartResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTargetGlobalPosition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/network.Network/GetTargetGlobalPosition',
            network__pb2.TargetRequest.SerializeToString,
            network__pb2.TargetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
