import json
import os
from abc import ABC
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, AsyncIterator, Self
from uuid import uuid7

from aiohttp import ClientSession
from aiohttp_sse_client.client import EventSource
from attr import field
from dacite import from_dict

from . import Error, MessageEnvelope


# signal-cli returns `{}` in `result` for these commands so this mirrors that.
# ref: https://github.com/AsamK/signal-cli/blob/3b784aa32be92b448d93fafb1cbe0727ad1d24eb/src/main/java/org/asamk/signal/jsonrpc/SignalJsonRpcCommandHandler.java#L275
@dataclass
class Empty:
    """
    Output type for commands which produce no output.
    """


@dataclass(frozen=True)
class RpcCommand[T](ABC):
    """Abstract base class for RPC commands."""

    @classmethod
    def __init_subclass__(cls, *, rpc_output_type: type[T]):
        cls.rpc_method: str = cls.__name__[0].upper() + cls.__name__[1:]
        cls.rpc_output_type = rpc_output_type

    def __init__(self) -> None:
        # https://stackoverflow.com/a/79182457
        raise NotImplementedError("Do not instantiate this class directly")


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
        response_obj = await self.post("rpc", json=asdict(request))
        response_dict = await response_obj.json()
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
