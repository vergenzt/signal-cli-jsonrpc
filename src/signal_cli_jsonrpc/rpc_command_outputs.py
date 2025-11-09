from collections import defaultdict
from dataclasses import dataclass, field
from signal_cli_jsonrpc.rpc_types import AttachmentData, Contact, SendMessageResult


# signal-cli returns `{}` in `result` for these commands so this mirrors that.
# ref: https://github.com/AsamK/signal-cli/blob/3b784aa32be92b448d93fafb1cbe0727ad1d24eb/src/main/java/org/asamk/signal/jsonrpc/SignalJsonRpcCommandHandler.java#L275
@dataclass
class Empty:
    """
    Output type for commands which produce no output.
    """


@dataclass
class UserStatus:
    recipient: str
    number: str | None
    username: str | None
    uuid: str
    is_Registered: bool


@dataclass
class JoinGroupResult:
    timestamp: int
    results: list[SendMessageResult]
    group_Id: str
    only_Requested: bool = False


@dataclass
class Device:
    id: int
    name: str
    created_timestamp: int
    last_seen_timestamp: int


@dataclass
class Identity:
    number: str
    uuid: str
    fingerprint: str
    safety_number: str
    scannable_safety_number: str
    trust_level: str
    added_timestamp: int


@dataclass
class UpdateGroupResult:
    timestamp: int | None = None
    results: list[SendMessageResult] = field(default_factory=list)
    group_id: str | None = None


@dataclass
class UploadStickerPackResult:
    url: str


# manually specified, not generated:
RPC_COMMAND_OUTPUT_TYPES = defaultdict(
    lambda: Empty,  # default
    {
        "GetAttachment": AttachmentData,
        "GetAvatar": AttachmentData,
        "GetSticker": AttachmentData,
        "GetUserStatus": list[UserStatus],
        "JoinGroup": JoinGroupResult,
        "ListContacts": list[Contact],
        "ListDevices": list[Device],
        "ListIdentities": list[Identity],
        "UpdateGroup": UpdateGroupResult,
        "UploadStickerPack": UploadStickerPackResult,
    },
)
