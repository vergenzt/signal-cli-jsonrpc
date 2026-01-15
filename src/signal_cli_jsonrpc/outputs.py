from collections import defaultdict
from dataclasses import dataclass, field
from typing import Literal

from .types import AttachmentData, Contact, SendMessageResult


@dataclass(frozen=True)
class Empty:
    """
    Output type for commands which produce no output.

    (Technically, `signal-cli` [returns an empty object (`{}`)]([1]) in the `result` field for these
    commands so this object mirrors that.)

    [[1]]: https://github.com/AsamK/signal-cli/blob/3b784aa32be92b448d93fafb1cbe0727ad1d24eb/src/main/java/org/asamk/signal/jsonrpc/SignalJsonRpcCommandHandler.java#L275
    """


@dataclass(frozen=True)
class UserStatus:
    recipient: str
    number: str | None
    username: str | None
    uuid: str
    is_Registered: bool


@dataclass(frozen=True)
class JoinGroupResult:
    timestamp: int
    results: list[SendMessageResult]
    group_Id: str
    only_Requested: bool = False


@dataclass
class GroupMember:
    number: str
    uuid: str


type GroupPermission = Literal["EVERY_MEMBER", "ONLY_ADMINS"]


@dataclass(frozen=True)
class Group:
    id: str
    name: str
    description: str | None
    is_member: bool
    is_blocked: bool
    message_expiration_time: int
    members: list[GroupMember]
    pending_members: list[GroupMember]
    requesting_members: list[GroupMember]
    admins: list[GroupMember]
    banned: list[GroupMember]
    permission_add_member: GroupPermission
    permission_edit_details: GroupPermission
    permission_send_message: GroupPermission
    group_invite_link: str | None


@dataclass(frozen=True)
class Device:
    id: int
    name: str
    created_timestamp: int
    last_seen_timestamp: int


@dataclass(frozen=True)
class Identity:
    number: str
    uuid: str
    fingerprint: str
    safety_number: str
    scannable_safety_number: str
    trust_level: str
    added_timestamp: int


@dataclass(frozen=True)
class UpdateGroupResult:
    timestamp: int | None = None
    results: list[SendMessageResult] = field(default_factory=list)
    group_id: str | None = None


@dataclass(frozen=True)
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
        "ListGroups": list[Group],
        "ListIdentities": list[Identity],
        "UpdateGroup": UpdateGroupResult,
        "UploadStickerPack": UploadStickerPackResult,
    },
)
