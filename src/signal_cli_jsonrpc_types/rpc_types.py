from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass(frozen=True, kw_only=True)
class Attachment:
    contentType: str | None
    filename: str | None
    id: str | None
    size: int | None
    width: int | None
    height: int | None
    caption: str | None
    uploadTimestamp: int | None


@dataclass(frozen=True, kw_only=True)
class AttachmentData:
    data: str | None


@dataclass(frozen=True, kw_only=True)
class CallMessage:
    offerMessage: Offer | None = None
    answerMessage: Answer | None = None
    busyMessage: Busy | None = None
    hangupMessage: Hangup | None = None
    iceUpdateMessages: tuple[IceUpdate | None, ...]

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
        deviceId: int

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
    givenName: str | None
    familyName: str | None
    nickName: str | None
    nickGivenName: str | None
    nickFamilyName: str | None
    note: str | None
    color: str | None
    isBlocked: bool
    isHidden: bool
    messageExpirationTime: int
    profileSharing: bool
    unregistered: bool
    profile: Profile | None
    internal: Internal | None = None

    @dataclass(frozen=True, kw_only=True)
    class Profile:
        lastUpdateTimestamp: int
        givenName: str | None
        familyName: str | None
        about: str | None
        aboutEmoji: str | None
        hasAvatar: bool
        mobileCoinAddress: str | None

    @dataclass(frozen=True, kw_only=True)
    class Internal:
        capabilities: tuple[str | None, ...]
        unidentifiedAccessMode: str | None
        sharesPhoneNumber: bool | None
        discoverableByPhonenumber: bool | None


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
    isProfile: bool


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
    expiresInSeconds: int | None
    viewOnce: bool | None = None
    reaction: Reaction | None = None
    quote: Quote | None = None
    payment: Payment | None = None
    mentions: tuple[Mention | None, ...] = ()
    previews: tuple[Preview | None, ...] = ()
    attachments: tuple[Attachment | None, ...] = ()
    sticker: Sticker | None = None
    remoteDelete: RemoteDelete | None = None
    contacts: tuple[SharedContact | None, ...] = ()
    textStyles: tuple[TextStyle | None, ...] = ()
    groupInfo: GroupInfo | None = None
    storyContext: StoryContext | None = None


@dataclass(frozen=True, kw_only=True)
class EditMessage:
    targetSentTimestamp: int
    dataMessage: DataMessage | None


@dataclass(frozen=True, kw_only=True)
class Error:
    message: str | None
    type: str | None


@dataclass(frozen=True, kw_only=True)
class GroupInfo:
    groupId: str | None
    groupName: str | None
    revision: int
    type: str | None


@dataclass(frozen=True, kw_only=True)
class Mention:
    name: str | None
    number: str | None
    uuid: str | None
    start: int
    length: int


@dataclass(frozen=True, kw_only=True)
class MessageEnvelope:
    source: str | None
    sourceNumber: str | None
    sourceUuid: str | None
    sourceName: str | None
    sourceDevice: int | None
    timestamp: int
    serverReceivedTimestamp: int
    serverDeliveredTimestamp: int
    dataMessage: DataMessage | None = None
    editMessage: EditMessage | None = None
    storyMessage: StoryMessage | None = None
    syncMessage: SyncMessage | None = None
    callMessage: CallMessage | None = None
    receiptMessage: ReceiptMessage | None = None
    typingMessage: TypingMessage | None = None


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
    authorNumber: str | None
    authorUuid: str | None
    text: str | None
    mentions: tuple[Mention | None, ...] = ()
    attachments: tuple[QuotedAttachment | None, ...]
    textStyles: tuple[TextStyle | None, ...] = ()


@dataclass(frozen=True, kw_only=True)
class QuotedAttachment:
    contentType: str | None
    filename: str | None
    thumbnail: Attachment | None = None


@dataclass(frozen=True, kw_only=True)
class Reaction:
    emoji: str | None
    targetAuthor: str | None
    targetAuthorNumber: str | None
    targetAuthorUuid: str | None
    targetSentTimestamp: int
    isRemove: bool


@dataclass(frozen=True, kw_only=True)
class ReceiptMessage:
    when: int
    isDelivery: bool
    isRead: bool
    isViewed: bool
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
    recipientAddress: RecipientAddress | None
    groupId: str | None = None
    type: Type | None
    token: str | None = None
    retryAfterSeconds: int | None = None

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
    packId: str | None
    stickerId: int


@dataclass(frozen=True, kw_only=True)
class StoryContext:
    authorNumber: str | None
    authorUuid: str | None
    sentTimestamp: int


@dataclass(frozen=True, kw_only=True)
class StoryMessage:
    allowsReplies: bool
    groupId: str | None = None
    fileAttachment: Attachment | None = None
    textAttachment: TextAttachment | None = None

    @dataclass(frozen=True, kw_only=True)
    class TextAttachment:
        text: str | None
        style: str | None = None
        textForegroundColor: str | None = None
        textBackgroundColor: str | None = None
        preview: Preview | None = None
        backgroundGradient: Gradient | None = None
        backgroundColor: str | None = None

        @dataclass(frozen=True, kw_only=True)
        class Gradient:
            startColor: str | None
            endColor: str | None
            colors: tuple[str | None, ...]
            positions: tuple[float | None, ...]
            angle: int | None


@dataclass(frozen=True, kw_only=True)
class SyncDataMessage:
    destination: str | None
    destinationNumber: str | None
    destinationUuid: str | None
    editMessage: EditMessage | None = None
    dataMessage: DataMessage | None


class SyncMessageType(StrEnum):
    CONTACTS_SYNC = auto()
    GROUPS_SYNC = auto()
    REQUEST_SYNC = auto()


@dataclass(frozen=True, kw_only=True)
class SyncMessage:
    sentMessage: SyncDataMessage | None = None
    sentStoryMessage: SyncStoryMessage | None = None
    blockedNumbers: tuple[str | None, ...] = ()
    blockedGroupIds: tuple[str | None, ...] = ()
    readMessages: tuple[SyncReadMessage | None, ...] = ()
    type: SyncMessageType | None = None


@dataclass(frozen=True, kw_only=True)
class SyncReadMessage:
    sender: str | None
    senderNumber: str | None
    senderUuid: str | None
    timestamp: int


@dataclass(frozen=True, kw_only=True)
class SyncStoryMessage:
    destinationNumber: str | None
    destinationUuid: str | None
    dataMessage: StoryMessage | None


@dataclass(frozen=True, kw_only=True)
class TextStyle:
    style: str | None
    start: int
    length: int


@dataclass(frozen=True, kw_only=True)
class TypingMessage:
    action: str | None
    timestamp: int
    groupId: str | None = None

