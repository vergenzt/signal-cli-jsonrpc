from dataclasses import dataclass
from enum import StrEnum, auto
from typing import TYPE_CHECKING, overload
from warnings import deprecated


@dataclass(frozen=True, kw_only=True)
class Attachment:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/db42f61cbb763c6e20ab6dc2fd47ae412b6fe953/src/main/java/org/asamk/signal/json/JsonAttachment.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/35def4445d13011f4feb9f6422546b88ce32bda0/src/main/java/org/asamk/signal/json/JsonAttachmentData.java)]*"""

    data: str | None


@dataclass(frozen=True, kw_only=True)
class CallMessage:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/be9efb9a25ab99bf28371dbbf91e9223cd2eaf92/src/main/java/org/asamk/signal/json/JsonCallMessage.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/e4c5144fbf46cc91a38f5011118e6008db894a80/src/main/java/org/asamk/signal/json/JsonContact.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9075cc1a309fbc90276d2878d480d1e9e9c81887/src/main/java/org/asamk/signal/json/JsonContactAddress.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9075cc1a309fbc90276d2878d480d1e9e9c81887/src/main/java/org/asamk/signal/json/JsonContactAvatar.java)]*"""

    attachment: Attachment | None
    is_profile: bool


@dataclass(frozen=True, kw_only=True)
class ContactEmail:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9075cc1a309fbc90276d2878d480d1e9e9c81887/src/main/java/org/asamk/signal/json/JsonContactEmail.java)]*"""

    value: str | None
    type: str | None
    label: str | None


@dataclass(frozen=True, kw_only=True)
class ContactName:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9afd4e43284e05a322aa261bcf4753eb96ba882a/src/main/java/org/asamk/signal/json/JsonContactName.java)]*"""

    nickname: str | None
    given: str | None
    family: str | None
    prefix: str | None
    suffix: str | None
    middle: str | None


@dataclass(frozen=True, kw_only=True)
class ContactPhone:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9075cc1a309fbc90276d2878d480d1e9e9c81887/src/main/java/org/asamk/signal/json/JsonContactPhone.java)]*"""

    value: str | None
    type: str | None
    label: str | None


@dataclass(frozen=True, kw_only=True)
class DataMessage:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/eac2a47163a07c2553fee8a0cfcdf3f1e6adafd2/src/main/java/org/asamk/signal/json/JsonDataMessage.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/0a287b0b3eef6591fed86fd4b39506e4d32eb69c/src/main/java/org/asamk/signal/json/JsonEditMessage.java)]*"""

    target_sent_timestamp: int
    data_message: DataMessage | None


@dataclass(frozen=True, kw_only=True)
class Error:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/ce7aa580b6f0580cdcf7fd68fcc8efba737d21ed/src/main/java/org/asamk/signal/json/JsonError.java)]*"""

    message: str | None
    type: str | None


@dataclass(frozen=True, kw_only=True)
class GroupInfo:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/eac2a47163a07c2553fee8a0cfcdf3f1e6adafd2/src/main/java/org/asamk/signal/json/JsonGroupInfo.java)]*"""

    group_id: str | None
    group_name: str | None
    revision: int
    type: str | None


@dataclass(frozen=True, kw_only=True)
class Mention:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/8867a7b9eeb3353d059613544899b262f4f47579/src/main/java/org/asamk/signal/json/JsonMention.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/json/JsonMessageEnvelope.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/62687d103fab1ade650b920008060c220361d581/src/main/java/org/asamk/signal/json/JsonPayment.java)]*"""

    note: str | None
    receipt: bytes


@dataclass(frozen=True, kw_only=True)
class Preview:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/b178c7c67aea7bf334cbf0d54a4666af0a65b5d9/src/main/java/org/asamk/signal/json/JsonPreview.java)]*"""

    url: str | None
    title: str | None
    description: str | None
    image: Attachment | None


@dataclass(frozen=True, kw_only=True)
class Quote:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/d51dd7ae575222b0baea7265c18ebc79f4a7b001/src/main/java/org/asamk/signal/json/JsonQuote.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9075cc1a309fbc90276d2878d480d1e9e9c81887/src/main/java/org/asamk/signal/json/JsonQuotedAttachment.java)]*"""

    content_type: str | None
    filename: str | None
    thumbnail: Attachment | None = None


@dataclass(frozen=True, kw_only=True)
class Reaction:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/8867a7b9eeb3353d059613544899b262f4f47579/src/main/java/org/asamk/signal/json/JsonReaction.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/32818a8608f5bddc46ad5c7dc442f509c939791c/src/main/java/org/asamk/signal/json/JsonReceiptMessage.java)]*"""

    when: int
    is_delivery: bool
    is_read: bool
    is_viewed: bool
    timestamps: tuple[int | None, ...]


@dataclass(frozen=True, kw_only=True)
class RecipientAddress:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/371dc068426ec8ecb9a7f6908a24d262bca729af/src/main/java/org/asamk/signal/json/JsonRecipientAddress.java)]*"""

    uuid: str | None
    number: str | None
    username: str | None


@dataclass(frozen=True, kw_only=True)
class RemoteDelete:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/9075cc1a309fbc90276d2878d480d1e9e9c81887/src/main/java/org/asamk/signal/json/JsonRemoteDelete.java)]*"""

    timestamp: int


@dataclass(frozen=True, kw_only=True)
class SendMessageResult:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/0c5993c0adde6b64206ba4f328a5b74e296791f3/src/main/java/org/asamk/signal/json/JsonSendMessageResult.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/d51dd7ae575222b0baea7265c18ebc79f4a7b001/src/main/java/org/asamk/signal/json/JsonSharedContact.java)]*"""

    name: ContactName | None
    avatar: ContactAvatar | None = None
    phone: tuple[ContactPhone | None, ...] = ()
    email: tuple[ContactEmail | None, ...] = ()
    address: tuple[ContactAddress | None, ...] = ()
    organization: str | None


@dataclass(frozen=True, kw_only=True)
class Sticker:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/beb3adcc72cd24b29688a931bf6246ab688249ea/src/main/java/org/asamk/signal/json/JsonSticker.java)]*"""

    pack_id: str | None
    sticker_id: int


@dataclass(frozen=True, kw_only=True)
class StoryContext:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/a593051512b716ed3cc42a1a7b69d49a459352ed/src/main/java/org/asamk/signal/json/JsonStoryContext.java)]*"""

    author_number: str | None
    author_uuid: str | None
    sent_timestamp: int


@dataclass(frozen=True, kw_only=True)
class StoryMessage:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/e5a67d6ce1312fe118e99b8bc8fb2f55ed1dbcf2/src/main/java/org/asamk/signal/json/JsonStoryMessage.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/0a287b0b3eef6591fed86fd4b39506e4d32eb69c/src/main/java/org/asamk/signal/json/JsonSyncDataMessage.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/eac2a47163a07c2553fee8a0cfcdf3f1e6adafd2/src/main/java/org/asamk/signal/json/JsonSyncMessage.java)]*"""

    CONTACTS_SYNC = auto()
    GROUPS_SYNC = auto()
    REQUEST_SYNC = auto()


@dataclass(frozen=True, kw_only=True)
class SyncMessage:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/eac2a47163a07c2553fee8a0cfcdf3f1e6adafd2/src/main/java/org/asamk/signal/json/JsonSyncMessage.java)]*"""

    sent_message: SyncDataMessage | None = None
    sent_story_message: SyncStoryMessage | None = None
    blocked_numbers: tuple[str | None, ...] = ()
    blocked_group_ids: tuple[str | None, ...] = ()
    read_messages: tuple[SyncReadMessage | None, ...] = ()
    type: SyncMessageType | None = None


@dataclass(frozen=True, kw_only=True)
class SyncReadMessage:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/8867a7b9eeb3353d059613544899b262f4f47579/src/main/java/org/asamk/signal/json/JsonSyncReadMessage.java)]*"""

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
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/a593051512b716ed3cc42a1a7b69d49a459352ed/src/main/java/org/asamk/signal/json/JsonSyncStoryMessage.java)]*"""

    destination_number: str | None
    destination_uuid: str | None


@dataclass(frozen=True, kw_only=True)
class TextStyle:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/91700ce995ae381dd97b246ea3ff11afb748e421/src/main/java/org/asamk/signal/json/JsonTextStyle.java)]*"""

    style: str | None
    start: int
    length: int


@dataclass(frozen=True, kw_only=True)
class TypingMessage:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/e5a67d6ce1312fe118e99b8bc8fb2f55ed1dbcf2/src/main/java/org/asamk/signal/json/JsonTypingMessage.java)]*"""

    action: str | None
    timestamp: int
    group_id: str | None = None


@dataclass(frozen=True, kw_only=True)
class FinishLinkParams:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/FinishLinkCommand.java)]*"""

    device_link_uri: str | None
    device_name: str | None


@dataclass(frozen=True, kw_only=True)
class FinishLink:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/FinishLinkCommand.java)]*"""

    number: str | None


@dataclass(frozen=True, kw_only=True)
class UserStatus:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/ca33249170118be0d2fe3e9deed4ad23b34ac875/src/main/java/org/asamk/signal/commands/GetUserStatusCommand.java)]*"""

    recipient: str | None
    number: str | None = None
    username: str | None = None
    uuid: str | None
    is_registered: bool


@dataclass(frozen=True, kw_only=True)
class Account:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListAccountsCommand.java)]*"""

    number: str | None


@dataclass(frozen=True, kw_only=True)
class Device:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListDevicesCommand.java)]*"""

    id: int
    name: str | None
    created_timestamp: int
    last_seen_timestamp: int


@dataclass(frozen=True, kw_only=True)
class Group:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/a22af8303a987905a3a6fb5ab78af11a2dc05b58/src/main/java/org/asamk/signal/commands/ListGroupsCommand.java)]*"""

    id: str | None
    name: str | None
    description: str | None
    is_member: bool
    is_blocked: bool
    message_expiration_time: int
    members: set[GroupMember | None]
    pending_members: set[GroupMember | None]
    requesting_members: set[GroupMember | None]
    admins: set[GroupMember | None]
    banned: set[GroupMember | None]
    permission_add_member: str | None
    permission_edit_details: str | None
    permission_send_message: str | None
    group_invite_link: str | None


@dataclass(frozen=True, kw_only=True)
class GroupMember:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/a22af8303a987905a3a6fb5ab78af11a2dc05b58/src/main/java/org/asamk/signal/commands/ListGroupsCommand.java)]*"""

    number: str | None
    uuid: str | None


@dataclass(frozen=True, kw_only=True)
class Identity:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListIdentitiesCommand.java)]*"""

    number: str | None
    uuid: str | None
    fingerprint: str | None
    safety_number: str | None
    scannable_safety_number: str | None
    trust_level: str | None
    added_timestamp: int


@dataclass(frozen=True, kw_only=True)
class StickerPack:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListStickerPacksCommand.java)]*"""

    pack_id: str | None
    url: str | None
    installed: bool
    title: str | None
    author: str | None
    cover: Sticker | None
    stickers: tuple[Sticker | None, ...]

    @dataclass(frozen=True, kw_only=True)
    class Sticker:
        id: int
        emoji: str | None
        content_type: str | None


class MessageRequestResponseType(StrEnum):
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/d84362eb0f022d8bd22321afb5f082b3881f316c/src/main/java/org/asamk/signal/commands/MessageRequestResponseType.java)]*"""

    ACCEPT = auto()
    DELETE = auto()


@dataclass(frozen=True, kw_only=True)
class ReceiveParams:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ReceiveCommand.java)]*"""

    timeout: float | None
    max_messages: int | None


class ReceiveMode(StrEnum):
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/81a11dc9776672e3468ee9a8eed556889fb2e070/src/main/java/org/asamk/signal/commands/ReceiveMode.java)]*"""

    ON_START = auto()
    ON_CONNECTION = auto()
    MANUAL = auto()


@dataclass(frozen=True, kw_only=True)
class RegistrationParams:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/RegisterCommand.java)]*"""

    voice: bool | None
    captcha: str | None
    reregister: bool | None


@dataclass(frozen=True, kw_only=True)
class Link:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/StartLinkCommand.java)]*"""

    device_link_uri: str | None


@dataclass(frozen=True, kw_only=True)
class AccountResponse:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UpdateAccountCommand.java)]*"""

    username: str | None = None
    username_link: str | None = None


@dataclass(frozen=True, kw_only=True)
class VerifyParams:
    """*[generated from [Java source](https://github.com/AsamK/signal-cli/blob/a0d5744c4945791eb57436d0f1288b09bd41132a/src/main/java/org/asamk/signal/commands/VerifyCommand.java)]*"""

    verification_code: str | None
    pin: str | None


__all__ = [
    "Attachment",
    "AttachmentData",
    "CallMessage",
    "Contact",
    "ContactAddress",
    "ContactAvatar",
    "ContactEmail",
    "ContactName",
    "ContactPhone",
    "DataMessage",
    "EditMessage",
    "Error",
    "GroupInfo",
    "Mention",
    "MessageEnvelope",
    "Payment",
    "Preview",
    "Quote",
    "QuotedAttachment",
    "Reaction",
    "ReceiptMessage",
    "RecipientAddress",
    "RemoteDelete",
    "SendMessageResult",
    "SharedContact",
    "Sticker",
    "StoryContext",
    "StoryMessage",
    "SyncDataMessage",
    "SyncMessageType",
    "SyncMessage",
    "SyncReadMessage",
    "SyncStoryMessage",
    "TextStyle",
    "TypingMessage",
    "FinishLinkParams",
    "FinishLink",
    "UserStatus",
    "Account",
    "Device",
    "Group",
    "GroupMember",
    "Identity",
    "StickerPack",
    "MessageRequestResponseType",
    "ReceiveParams",
    "ReceiveMode",
    "RegistrationParams",
    "Link",
    "AccountResponse",
    "VerifyParams",
]
