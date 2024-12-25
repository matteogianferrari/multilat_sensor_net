# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: dist_network.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'dist_network.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x64ist_network.proto\x12\x0c\x64ist_network\"\"\n\rTargetRequest\x12\x11\n\tclient_id\x18\x01 \x01(\x05\"]\n\x0eTargetResponse\x12*\n\x06status\x18\x01 \x01(\x0e\x32\x1a.dist_network.TargetStatus\x12\t\n\x01x\x18\x02 \x01(\x02\x12\t\n\x01y\x18\x03 \x01(\x02\x12\t\n\x01z\x18\x04 \x01(\x02\"U\n\x0bNodeRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\t\n\x01x\x18\x02 \x01(\x02\x12\t\n\x01y\x18\x03 \x01(\x02\x12\t\n\x01z\x18\x04 \x01(\x02\x12\x14\n\x0c\x62ind_address\x18\x05 \x01(\t\"8\n\x0cNodeResponse\x12(\n\x06status\x18\x01 \x01(\x0e\x32\x18.dist_network.NodeStatus\"!\n\x0cStartRequest\x12\x11\n\tclient_id\x18\x01 \x01(\x05\"H\n\rStartResponse\x12&\n\x06status\x18\x01 \x01(\x0e\x32\x16.dist_network.SNStatus\x12\x0f\n\x07n_nodes\x18\x02 \x01(\x05*7\n\x0cTargetStatus\x12\x0e\n\nTS_UNKNOWN\x10\x00\x12\t\n\x05TS_OK\x10\x01\x12\x0c\n\x08TS_ERROR\x10\x02*5\n\nNodeStatus\x12\x0e\n\nNS_UNKNOWN\x10\x00\x12\t\n\x05NS_OK\x10\x01\x12\x0c\n\x08NS_ERROR\x10\x02*3\n\x08SNStatus\x12\x0e\n\nSS_UNKNOWN\x10\x00\x12\t\n\x05SS_OK\x10\x01\x12\x0c\n\x08SS_ERROR\x10\x02\x32\xf4\x01\n\x0b\x44istNetwork\x12\x42\n\x07\x41\x64\x64Node\x12\x19.dist_network.NodeRequest\x1a\x1a.dist_network.NodeResponse\"\x00\x12I\n\x0cStartNetwork\x12\x1a.dist_network.StartRequest\x1a\x1b.dist_network.StartResponse\"\x00\x12V\n\x17GetTargetGlobalPosition\x12\x1b.dist_network.TargetRequest\x1a\x1c.dist_network.TargetResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dist_network_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TARGETSTATUS']._serialized_start=421
  _globals['_TARGETSTATUS']._serialized_end=476
  _globals['_NODESTATUS']._serialized_start=478
  _globals['_NODESTATUS']._serialized_end=531
  _globals['_SNSTATUS']._serialized_start=533
  _globals['_SNSTATUS']._serialized_end=584
  _globals['_TARGETREQUEST']._serialized_start=36
  _globals['_TARGETREQUEST']._serialized_end=70
  _globals['_TARGETRESPONSE']._serialized_start=72
  _globals['_TARGETRESPONSE']._serialized_end=165
  _globals['_NODEREQUEST']._serialized_start=167
  _globals['_NODEREQUEST']._serialized_end=252
  _globals['_NODERESPONSE']._serialized_start=254
  _globals['_NODERESPONSE']._serialized_end=310
  _globals['_STARTREQUEST']._serialized_start=312
  _globals['_STARTREQUEST']._serialized_end=345
  _globals['_STARTRESPONSE']._serialized_start=347
  _globals['_STARTRESPONSE']._serialized_end=419
  _globals['_DISTNETWORK']._serialized_start=587
  _globals['_DISTNETWORK']._serialized_end=831
# @@protoc_insertion_point(module_scope)