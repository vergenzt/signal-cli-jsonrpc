from dataclasses import dataclass
from enum import StrEnum, auto
from typing import TYPE_CHECKING, overload
from warnings import deprecated


@dataclass(frozen=True, kw_only=True)
class Attachment:
    content_type: str | None
    filename: str | None
    id: str | None
    size: int | None
    width: int | None
    height: int | None
    caption: str | None
    upload_timestamp: int | None


@dataclass(frozen=True, kw_only=True)
class AttachmentData:
    data: str | None


@dataclass(frozen=True, kw_only=True)
class CallMessage:
    offer_message: Offer | None = None
    answer_message: Answer | None = None
    busy_message: Busy | None = None
    hangup_message: Hangup | None = None
    ice_update_messages: tuple[IceUpdate | None, ...] = ()

    @dataclass(frozen=True, kw_only=True)
    class Offer:
        id: int
        type: str | None
        opaque: str | None

    @dataclass(frozen=True, kw_only=True)
    class Answer:
        id: int
        opaque: str | None

    @dataclass(frozen=True, kw_only=True)
    class Busy:
        id: int

    @dataclass(frozen=True, kw_only=True)
    class Hangup:
        id: int
        type: str | None
        device_id: int

    @dataclass(frozen=True, kw_only=True)
    class IceUpdate:
        id: int
        opaque: str | None


@dataclass(frozen=True, kw_only=True)
class Contact:
    number: str | None
    uuid: str | None
    username: str | None
    name: str | None
    given_name: str | None
    family_name: str | None
    nick_name: str | None
    nick_given_name: str | None
    nick_family_name: str | None
    note: str | None
    color: str | None
    is_blocked: bool
    is_hidden: bool
    message_expiration_time: int
    profile_sharing: bool
    unregistered: bool
    profile: Profile | None
    internal: Internal | None = None

    @dataclass(frozen=True, kw_only=True)
    class Profile:
        last_update_timestamp: int
        given_name: str | None
        family_name: str | None
        about: str | None
        about_emoji: str | None
        has_avatar: bool
        mobile_coin_address: str | None

    @dataclass(frozen=True, kw_only=True)
    class Internal:
        capabilities: tuple[str | None, ...]
        unidentified_access_mode: str | None
        shares_phone_number: bool | None
        discoverable_by_phonenumber: bool | None


@dataclass(frozen=True, kw_only=True)
class ContactAddress:
    type: str | None
    label: str | None
    street: str | None
    pobox: str | None
    neighborhood: str | None
    city: str | None
    region: str | None
    postcode: str | None
    country: str | None


@dataclass(frozen=True, kw_only=True)
class ContactAvatar:
    attachment: Attachment | None
    is_profile: bool


@dataclass(frozen=True, kw_only=True)
class ContactEmail:
    value: str | None
    type: str | None
    label: str | None


@dataclass(frozen=True, kw_only=True)
class ContactName:
    nickname: str | None
    given: str | None
    family: str | None
    prefix: str | None
    suffix: str | None
    middle: str | None


@dataclass(frozen=True, kw_only=True)
class ContactPhone:
    value: str | None
    type: str | None
    label: str | None


@dataclass(frozen=True, kw_only=True)
class DataMessage:
    timestamp: int
    message: str | None
    expires_in_seconds: int | None
    view_once: bool | None = None
    reaction: Reaction | None = None
    quote: Quote | None = None
    payment: Payment | None = None
    mentions: tuple[Mention | None, ...] = ()
    previews: tuple[Preview | None, ...] = ()
    attachments: tuple[Attachment | None, ...] = ()
    sticker: Sticker | None = None
    remote_delete: RemoteDelete | None = None
    contacts: tuple[SharedContact | None, ...] = ()
    text_styles: tuple[TextStyle | None, ...] = ()
    group_info: GroupInfo | None = None
    story_context: StoryContext | None = None


@dataclass(frozen=True, kw_only=True)
class EditMessage:
    target_sent_timestamp: int
    data_message: DataMessage | None


@dataclass(frozen=True, kw_only=True)
class Error:
    message: str | None
    type: str | None


@dataclass(frozen=True, kw_only=True)
class GroupInfo:
    group_id: str | None
    group_name: str | None
    revision: int
    type: str | None


@dataclass(frozen=True, kw_only=True)
class Mention:
    name: str | None
    if TYPE_CHECKING:

        @property
        @overload
        @deprecated("Deprecated")
        def name(self) -> str | None: ...

    number: str | None
    uuid: str | None
    start: int
    length: int


@dataclass(frozen=True, kw_only=True)
class MessageEnvelope:
    source: str | None
    if TYPE_CHECKING:

        @property
        @overload
        @deprecated("Deprecated")
        def source(self) -> str | None: ...

    source_number: str | None
    source_uuid: str | None
    source_name: str | None
    source_device: int | None
    timestamp: int
    server_received_timestamp: int
    server_delivered_timestamp: int
    data_message: DataMessage | None = None
    edit_message: EditMessage | None = None
    story_message: StoryMessage | None = None
    sync_message: SyncMessage | None = None
    call_message: CallMessage | None = None
    receipt_message: ReceiptMessage | None = None
    typing_message: TypingMessage | None = None


@dataclass(frozen=True, kw_only=True)
class Payment:
    note: str | None
    receipt: bytes


@dataclass(frozen=True, kw_only=True)
class Preview:
    url: str | None
    title: str | None
    description: str | None
    image: Attachment | None


@dataclass(frozen=True, kw_only=True)
class Quote:
    id: int
    author: str | None
    if TYPE_CHECKING:

        @property
        @overload
        @deprecated("Deprecated")
        def author(self) -> str | None: ...

    author_number: str | None
    author_uuid: str | None
    text: str | None
    mentions: tuple[Mention | None, ...] = ()
    attachments: tuple[QuotedAttachment | None, ...]
    text_styles: tuple[TextStyle | None, ...] = ()


@dataclass(frozen=True, kw_only=True)
class QuotedAttachment:
    content_type: str | None
    filename: str | None
    thumbnail: Attachment | None = None


@dataclass(frozen=True, kw_only=True)
class Reaction:
    emoji: str | None
    target_author: str | None
    if TYPE_CHECKING:

        @property
        @overload
        @deprecated("Deprecated")
        def target_author(self) -> str | None: ...

    target_author_number: str | None
    target_author_uuid: str | None
    target_sent_timestamp: int
    is_remove: bool


@dataclass(frozen=True, kw_only=True)
class ReceiptMessage:
    when: int
    is_delivery: bool
    is_read: bool
    is_viewed: bool
    timestamps: tuple[int | None, ...]


@dataclass(frozen=True, kw_only=True)
class RecipientAddress:
    uuid: str | None
    number: str | None
    username: str | None


@dataclass(frozen=True, kw_only=True)
class RemoteDelete:
    timestamp: int


@dataclass(frozen=True, kw_only=True)
class SendMessageResult:
    recipient_address: RecipientAddress | None
    group_id: str | None = None
    type: Type | None
    token: str | None = None
    retry_after_seconds: int | None = None

    class Type(StrEnum):
        SUCCESS = auto()
        NETWORK_FAILURE = auto()
        UNREGISTERED_FAILURE = auto()
        IDENTITY_FAILURE = auto()
        RATE_LIMIT_FAILURE = auto()
        INVALID_PRE_KEY_FAILURE = auto()


@dataclass(frozen=True, kw_only=True)
class SharedContact:
    name: ContactName | None
    avatar: ContactAvatar | None = None
    phone: tuple[ContactPhone | None, ...] = ()
    email: tuple[ContactEmail | None, ...] = ()
    address: tuple[ContactAddress | None, ...] = ()
    organization: str | None


@dataclass(frozen=True, kw_only=True)
class Sticker:
    pack_id: str | None
    sticker_id: int


@dataclass(frozen=True, kw_only=True)
class StoryContext:
    author_number: str | None
    author_uuid: str | None
    sent_timestamp: int


@dataclass(frozen=True, kw_only=True)
class StoryMessage:
    allows_replies: bool
    group_id: str | None = None
    file_attachment: Attachment | None = None
    text_attachment: TextAttachment | None = None

    @dataclass(frozen=True, kw_only=True)
    class TextAttachment:
        text: str | None
        style: str | None = None
        text_foreground_color: str | None = None
        text_background_color: str | None = None
        preview: Preview | None = None
        background_gradient: Gradient | None = None
        background_color: str | None = None

        @dataclass(frozen=True, kw_only=True)
        class Gradient:
            start_color: str | None
            end_color: str | None
            colors: tuple[str | None, ...]
            positions: tuple[float | None, ...]
            angle: int | None


@dataclass(frozen=True, kw_only=True)
class SyncDataMessage(DataMessage):
    destination: str | None
    if TYPE_CHECKING:

        @property
        @overload
        @deprecated("Deprecated")
        def destination(self) -> str | None: ...

    destination_number: str | None
    destination_uuid: str | None
    edit_message: EditMessage | None = None


class SyncMessageType(StrEnum):
    CONTACTS_SYNC = auto()
    GROUPS_SYNC = auto()
    REQUEST_SYNC = auto()


@dataclass(frozen=True, kw_only=True)
class SyncMessage:
    sent_message: SyncDataMessage | None = None
    sent_story_message: SyncStoryMessage | None = None
    blocked_numbers: tuple[str | None, ...] = ()
    blocked_group_ids: tuple[str | None, ...] = ()
    read_messages: tuple[SyncReadMessage | None, ...] = ()
    type: SyncMessageType | None = None


@dataclass(frozen=True, kw_only=True)
class SyncReadMessage:
    sender: str | None
    if TYPE_CHECKING:

        @property
        @overload
        @deprecated("Deprecated")
        def sender(self) -> str | None: ...

    sender_number: str | None
    sender_uuid: str | None
    timestamp: int


@dataclass(frozen=True, kw_only=True)
class SyncStoryMessage(StoryMessage):
    destination_number: str | None
    destination_uuid: str | None


@dataclass(frozen=True, kw_only=True)
class TextStyle:
    style: str | None
    start: int
    length: int


@dataclass(frozen=True, kw_only=True)
class TypingMessage:
    action: str | None
    timestamp: int
    group_id: str | None = None

