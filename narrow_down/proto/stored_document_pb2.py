# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/stored_document.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1bproto/stored_document.proto\x12\x0fstored_document"\xac\x01\n\x13StoredDocumentProto\x12\x10\n\x03id_\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x15\n\x08\x64ocument\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nexact_part\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x13\n\x0b\x66ingerprint\x18\x04 \x03(\r\x12\x11\n\x04\x64\x61ta\x18\x05 \x01(\tH\x03\x88\x01\x01\x42\x06\n\x04_id_B\x0b\n\t_documentB\r\n\x0b_exact_partB\x07\n\x05_datab\x06proto3'
)


_STOREDDOCUMENTPROTO = DESCRIPTOR.message_types_by_name["StoredDocumentProto"]
StoredDocumentProto = _reflection.GeneratedProtocolMessageType(
    "StoredDocumentProto",
    (_message.Message,),
    {
        "DESCRIPTOR": _STOREDDOCUMENTPROTO,
        "__module__": "proto.stored_document_pb2"
        # @@protoc_insertion_point(class_scope:stored_document.StoredDocumentProto)
    },
)
_sym_db.RegisterMessage(StoredDocumentProto)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _STOREDDOCUMENTPROTO._serialized_start = 49
    _STOREDDOCUMENTPROTO._serialized_end = 221
# @@protoc_insertion_point(module_scope)
