"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class StoredDocumentProto(google.protobuf.message.Message):
    """StoredDocumentProto is a protobuf representation of narrow_down.data_types.StoredDocument"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID__FIELD_NUMBER: builtins.int
    DOCUMENT_FIELD_NUMBER: builtins.int
    EXACT_PART_FIELD_NUMBER: builtins.int
    FINGERPRINT_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    id_: builtins.int
    document: builtins.str
    exact_part: builtins.str
    @property
    def fingerprint(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    data: builtins.str
    def __init__(
        self,
        *,
        id_: builtins.int | None = ...,
        document: builtins.str | None = ...,
        exact_part: builtins.str | None = ...,
        fingerprint: collections.abc.Iterable[builtins.int] | None = ...,
        data: builtins.str | None = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "_data",
            b"_data",
            "_document",
            b"_document",
            "_exact_part",
            b"_exact_part",
            "_id_",
            b"_id_",
            "data",
            b"data",
            "document",
            b"document",
            "exact_part",
            b"exact_part",
            "id_",
            b"id_",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "_data",
            b"_data",
            "_document",
            b"_document",
            "_exact_part",
            b"_exact_part",
            "_id_",
            b"_id_",
            "data",
            b"data",
            "document",
            b"document",
            "exact_part",
            b"exact_part",
            "fingerprint",
            b"fingerprint",
            "id_",
            b"id_",
        ],
    ) -> None: ...
    @typing.overload
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["_data", b"_data"]
    ) -> typing_extensions.Literal["data"] | None: ...
    @typing.overload
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["_document", b"_document"]
    ) -> typing_extensions.Literal["document"] | None: ...
    @typing.overload
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["_exact_part", b"_exact_part"]
    ) -> typing_extensions.Literal["exact_part"] | None: ...
    @typing.overload
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["_id_", b"_id_"]
    ) -> typing_extensions.Literal["id_"] | None: ...

global___StoredDocumentProto = StoredDocumentProto
