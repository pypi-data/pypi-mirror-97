# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Mapping as typing___Mapping,
    MutableMapping as typing___MutableMapping,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


class Program(google___protobuf___message___Message):

    @property
    def language(self) -> Language: ...

    @property
    def circuit(self) -> Circuit: ...

    @property
    def schedule(self) -> Schedule: ...

    @property
    def constants(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[Constant]: ...

    def __init__(self,
        language : typing___Optional[Language] = None,
        circuit : typing___Optional[Circuit] = None,
        schedule : typing___Optional[Schedule] = None,
        constants : typing___Optional[typing___Iterable[Constant]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Program: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"circuit",u"language",u"program",u"schedule"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"circuit",u"constants",u"language",u"program",u"schedule"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"circuit",b"circuit",u"language",b"language",u"program",b"program",u"schedule",b"schedule"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[b"circuit",b"constants",b"language",b"program",b"schedule"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"program",b"program"]) -> typing_extensions___Literal["circuit","schedule"]: ...

class Constant(google___protobuf___message___Message):
    string_value = ... # type: typing___Text

    def __init__(self,
        string_value : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Constant: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"string_value"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"string_value"]) -> None: ...

class Circuit(google___protobuf___message___Message):
    class SchedulingStrategy(int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: int) -> str: ...
        @classmethod
        def Value(cls, name: str) -> Circuit.SchedulingStrategy: ...
        @classmethod
        def keys(cls) -> typing___List[str]: ...
        @classmethod
        def values(cls) -> typing___List[Circuit.SchedulingStrategy]: ...
        @classmethod
        def items(cls) -> typing___List[typing___Tuple[str, Circuit.SchedulingStrategy]]: ...
    SCHEDULING_STRATEGY_UNSPECIFIED = typing___cast(SchedulingStrategy, 0)
    MOMENT_BY_MOMENT = typing___cast(SchedulingStrategy, 1)

    scheduling_strategy = ... # type: Circuit.SchedulingStrategy

    @property
    def moments(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[Moment]: ...

    def __init__(self,
        scheduling_strategy : typing___Optional[Circuit.SchedulingStrategy] = None,
        moments : typing___Optional[typing___Iterable[Moment]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Circuit: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"moments",u"scheduling_strategy"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"moments",b"scheduling_strategy"]) -> None: ...

class Moment(google___protobuf___message___Message):

    @property
    def operations(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[Operation]: ...

    def __init__(self,
        operations : typing___Optional[typing___Iterable[Operation]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Moment: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"operations"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"operations"]) -> None: ...

class Schedule(google___protobuf___message___Message):

    @property
    def scheduled_operations(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ScheduledOperation]: ...

    def __init__(self,
        scheduled_operations : typing___Optional[typing___Iterable[ScheduledOperation]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Schedule: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"scheduled_operations"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"scheduled_operations"]) -> None: ...

class ScheduledOperation(google___protobuf___message___Message):
    start_time_picos = ... # type: int

    @property
    def operation(self) -> Operation: ...

    def __init__(self,
        operation : typing___Optional[Operation] = None,
        start_time_picos : typing___Optional[int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ScheduledOperation: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"operation"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"operation",u"start_time_picos"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"operation",b"operation"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[b"operation",b"start_time_picos"]) -> None: ...

class Language(google___protobuf___message___Message):
    gate_set = ... # type: typing___Text
    arg_function_language = ... # type: typing___Text

    def __init__(self,
        gate_set : typing___Optional[typing___Text] = None,
        arg_function_language : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Language: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"arg_function_language",u"gate_set"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"arg_function_language",b"gate_set"]) -> None: ...

class Operation(google___protobuf___message___Message):
    class ArgsEntry(google___protobuf___message___Message):
        key = ... # type: typing___Text

        @property
        def value(self) -> Arg: ...

        def __init__(self,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[Arg] = None,
            ) -> None: ...
        @classmethod
        def FromString(cls, s: bytes) -> Operation.ArgsEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        if sys.version_info >= (3,):
            def HasField(self, field_name: typing_extensions___Literal[u"value"]) -> bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",u"value"]) -> None: ...
        else:
            def HasField(self, field_name: typing_extensions___Literal[u"value",b"value"]) -> bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[b"key",b"value"]) -> None: ...

    token_value = ... # type: typing___Text
    token_constant_index = ... # type: int

    @property
    def gate(self) -> Gate: ...

    @property
    def args(self) -> typing___MutableMapping[typing___Text, Arg]: ...

    @property
    def qubits(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[Qubit]: ...

    def __init__(self,
        gate : typing___Optional[Gate] = None,
        args : typing___Optional[typing___Mapping[typing___Text, Arg]] = None,
        qubits : typing___Optional[typing___Iterable[Qubit]] = None,
        token_value : typing___Optional[typing___Text] = None,
        token_constant_index : typing___Optional[int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Operation: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"gate",u"token",u"token_constant_index",u"token_value"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"args",u"gate",u"qubits",u"token",u"token_constant_index",u"token_value"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"gate",b"gate",u"token",b"token",u"token_constant_index",b"token_constant_index",u"token_value",b"token_value"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[b"args",b"gate",b"qubits",b"token",b"token_constant_index",b"token_value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"token",b"token"]) -> typing_extensions___Literal["token_value","token_constant_index"]: ...

class Gate(google___protobuf___message___Message):
    id = ... # type: typing___Text

    def __init__(self,
        id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Gate: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"id"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"id"]) -> None: ...

class Qubit(google___protobuf___message___Message):
    id = ... # type: typing___Text

    def __init__(self,
        id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Qubit: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"id"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"id"]) -> None: ...

class Arg(google___protobuf___message___Message):
    symbol = ... # type: typing___Text
    constant_index = ... # type: int

    @property
    def arg_value(self) -> ArgValue: ...

    @property
    def func(self) -> ArgFunction: ...

    def __init__(self,
        arg_value : typing___Optional[ArgValue] = None,
        symbol : typing___Optional[typing___Text] = None,
        func : typing___Optional[ArgFunction] = None,
        constant_index : typing___Optional[int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Arg: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"arg",u"arg_value",u"constant_index",u"func",u"symbol"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"arg",u"arg_value",u"constant_index",u"func",u"symbol"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"arg",b"arg",u"arg_value",b"arg_value",u"constant_index",b"constant_index",u"func",b"func",u"symbol",b"symbol"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[b"arg",b"arg_value",b"constant_index",b"func",b"symbol"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"arg",b"arg"]) -> typing_extensions___Literal["arg_value","symbol","func","constant_index"]: ...

class ArgValue(google___protobuf___message___Message):
    float_value = ... # type: float
    string_value = ... # type: typing___Text
    double_value = ... # type: float

    @property
    def bool_values(self) -> RepeatedBoolean: ...

    def __init__(self,
        float_value : typing___Optional[float] = None,
        bool_values : typing___Optional[RepeatedBoolean] = None,
        string_value : typing___Optional[typing___Text] = None,
        double_value : typing___Optional[float] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ArgValue: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"arg_value",u"bool_values",u"double_value",u"float_value",u"string_value"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"arg_value",u"bool_values",u"double_value",u"float_value",u"string_value"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"arg_value",b"arg_value",u"bool_values",b"bool_values",u"double_value",b"double_value",u"float_value",b"float_value",u"string_value",b"string_value"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[b"arg_value",b"bool_values",b"double_value",b"float_value",b"string_value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"arg_value",b"arg_value"]) -> typing_extensions___Literal["float_value","bool_values","string_value","double_value"]: ...

class RepeatedBoolean(google___protobuf___message___Message):
    values = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[bool]

    def __init__(self,
        values : typing___Optional[typing___Iterable[bool]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> RepeatedBoolean: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"values"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"values"]) -> None: ...

class ArgFunction(google___protobuf___message___Message):
    type = ... # type: typing___Text

    @property
    def args(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[Arg]: ...

    def __init__(self,
        type : typing___Optional[typing___Text] = None,
        args : typing___Optional[typing___Iterable[Arg]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ArgFunction: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"args",u"type"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[b"args",b"type"]) -> None: ...
