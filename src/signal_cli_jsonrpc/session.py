import json
import os
from abc import ABCMeta
from dataclasses import asdict, dataclass
from types import GenericAlias
from typing import TYPE_CHECKING, Any, AsyncIterator, Self
from uuid import uuid7

from aiohttp import ClientSession
from aiohttp_sse_client.client import EventSource
from attr import field
from caseutil import to_camel, to_snake
from dacite import from_dict

from .types import Error, MessageEnvelope
from .utils import dict_transform_keys


class _RpcCommandMeta[OutputType](ABCMeta):
    _rpc_method_name: str
    _rpc_output_type: type[OutputType]

    def __init__(cls, name: str, bases: tuple[type, ...], nsp: dict[str, Any], /, **kw: Any):
        match cls:
            # no type var needed to create RpcCommand base class
            case type(__name__="RpcCommand"):
                pass

            # but for all others, expect base class to be passed as `RpcCommand[<output_type>]`
            case type(
                __name__=rpc_method_name_pascal,
                __orig_bases__=[
                    GenericAlias(
                        __origin__=_RpcCommandMeta(),  # instance of `_RpcCommandMeta`, i.e. `RpcCommand` itself
                        __args__=[OutputType],
                    )
                ],
            ):
                cls._rpc_method_name = (
                    rpc_method_name_pascal[0].lower() + rpc_method_name_pascal[1:]
                )
                cls._rpc_output_type = OutputType

            case name, (base, *_):
                breakpoint()
                raise TypeError(f"Cannot create {cls} as subclass of {base} without generic arg!")

        return super().__init__(name, bases, nsp, **kw)


@dataclass(frozen=True)
class RpcCommand[OutputType](metaclass=_RpcCommandMeta):
    """Abstract base class for RPC commands. Subclasses must specify `OutputType` type parameter."""

    async def do(self, session: SignalCliRPCSession) -> RpcResponse[OutputType]:
        return await session.rpc(self)

    async def get(self, session: SignalCliRPCSession) -> OutputType:
        return await session.rpc_output(self)


@dataclass(frozen=True)
class RpcRequest[T]:
    method: str
    params: T
    id: str | None = field(factory=lambda: str(uuid7()))


@dataclass(frozen=True)
class RpcResponseOk[T]:
    result: T
    id: str | None = None


@dataclass(frozen=True)
class RpcResponseError(Exception):
    error: Any
    id: str | None = None


type RpcResponse[T] = RpcResponseOk[T] | RpcResponseError

type RpcMessage = RpcRequest | RpcResponse | list[RpcMessage]


@dataclass(frozen=True)
class _RpcMessageWrapper[T: RpcMessage]:
    "Helper to allow deserializing a top-level union with `from_dict`"

    _: T

    def __iter__(self):
        if isinstance(self._, list):
            yield from self._
        else:
            yield self._


@dataclass
class MessageError:
    account: str
    error: Error | None


@dataclass
class Message:
    account: str
    envelope: MessageEnvelope | None


type MessageOrError = Message | MessageError


class SignalCliRPCSession(ClientSession):
    def __init__(self, *args, **kwargs) -> None:
        base_url = os.environ["SIGNAL_CLI_ADDR"] + "/api/v1/"
        super().__init__(base_url, *args, **kwargs)

    if TYPE_CHECKING:
        # narrow return type so our custom methods can be called on result
        async def __aenter__(self) -> Self: ...

    @property
    async def signal_cli_events(self) -> AsyncIterator[MessageOrError]:
        async with EventSource("events", session=self) as sse_events:
            async for sse_event in sse_events:
                signal_event = from_dict(MessageOrError, json.loads(sse_event.data))
                yield signal_event

    async def rpc[OutputT](self, command: RpcCommand[OutputT]) -> RpcResponse[OutputT]:
        request = RpcRequest(command._rpc_method_name, command)
        response_obj = await self.post("rpc", json=dict_transform_keys(to_camel, asdict(request)))
        response_dict = dict_transform_keys(to_snake, await response_obj.json())
        output_type = command._rpc_output_type
        response = from_dict(_RpcMessageWrapper[RpcResponse[output_type]], response_dict)._
        assert response.id == request.id
        return response

    async def rpc_output[OutputT](self, command: RpcCommand[OutputT]) -> OutputT:
        match await self.rpc(command):
            case RpcResponseOk(result):
                return result
            case RpcResponseError() as error:
                raise error
