import json
import os
from abc import ABCMeta
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Self
from uuid import uuid7

from aiohttp import ClientSession
from aiohttp_sse_client.client import EventSource
from attr import field
from caseutil import to_camel, to_snake
from dacite import from_dict

from .rpc_types import Error, MessageEnvelope


class RpcCommandMeta[T](ABCMeta):
    rpc_method: str
    rpc_output_type: type[T]

    def __init__(cls, rpc_output_type: type[T]):
        cls.rpc_method = cls.__name__[0].upper() + cls.__name__[1:]
        cls.rpc_output_type = rpc_output_type


@dataclass(frozen=True)
class RpcCommand(metaclass=RpcCommandMeta):
    """Abstract base class for RPC commands. Subclasses must pass `rpc_output_type` parameter."""


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


def dict_transform_keys(transform: Callable[[str], str], dct: dict[str, Any]) -> dict[str, Any]:
    return {
        transform(k): (dict_transform_keys(transform, v) if isinstance(v, dict) else v)
        for k, v in dct.items()
    }


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
class SignalCliEvent:
    account: str
    error: Error | None
    envelope: MessageEnvelope | None


class SignalCliRPCSession(ClientSession):
    def __init__(self, *args, **kwargs) -> None:
        base_url = os.environ["SIGNAL_CLI_ADDR"] + "/api/v1/"
        super().__init__(base_url, *args, **kwargs)

    if TYPE_CHECKING:
        # narrow return type so our custom methods can be called on result
        async def __aenter__(self) -> Self: ...

    @property
    async def signal_cli_events(self) -> AsyncIterator[SignalCliEvent]:
        async with EventSource("events", session=self) as sse_events:
            async for sse_event in sse_events:
                signal_event = from_dict(SignalCliEvent, json.loads(sse_event.data))
                yield signal_event

    async def rpc[OutputT](self, command: RpcCommand[OutputT]) -> RpcResponse[OutputT]:
        request = RpcRequest(command.rpc_method, command)
        response_obj = await self.post("rpc", json=dict_transform_keys(to_camel, asdict(request)))
        response_dict = dict_transform_keys(to_snake, await response_obj.json())
        output_type = command.rpc_output_type
        response = from_dict(_RpcMessageWrapper[RpcResponse[output_type]], response_dict)._
        assert response.id == request.id
        return response

    async def rpc_output[OutputT](self, command: RpcCommand[OutputT]) -> OutputT:
        match await self.rpc(command):
            case RpcResponseOk(result):
                return result
            case RpcResponseError() as error:
                raise error
