from dataclasses import dataclass
from enum import StrEnum, auto

_dataclass = dataclass(frozen=True, kw_only=True)


@_dataclass
class Attachment:
    contentType: str | None
    filename: str | None
    id: str | None
    size: int | None
    width: int | None
    height: int | None
    caption: str | None
    uploadTimestamp: int | None


@_dataclass
class AttachmentData:
    data: str | None


@_dataclass
class CallMessage:
    offerMessage: Offer | None = None
    answerMessage: Answer | None = None
    busyMessage: Busy | None = None
    hangupMessage: Hangup | None = None
    iceUpdateMessages: tuple[IceUpdate | None, ...]

    @_dataclass
    class Offer:
        id: int
        type: str | None
        opaque: str | None

    @_dataclass
    class Answer:
        id: int
        opaque: str | None

    @_dataclass
    class Busy:
        id: int

    @_dataclass
    class Hangup:
        id: int
        type: str | None
        deviceId: int

    @_dataclass
    class IceUpdate:
        id: int
        opaque: str | None


@_dataclass
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

    @_dataclass
    class Profile:
        lastUpdateTimestamp: int
        givenName: str | None
        familyName: str | None
        about: str | None
        aboutEmoji: str | None
        hasAvatar: bool
        mobileCoinAddress: str | None

    @_dataclass
    class Internal:
        capabilities: tuple[str | None, ...]
        unidentifiedAccessMode: str | None
        sharesPhoneNumber: bool | None
        discoverableByPhonenumber: bool | None


@_dataclass
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


@_dataclass
class ContactAvatar:
    attachment: Attachment | None
    isProfile: bool


@_dataclass
class ContactEmail:
    value: str | None
    type: str | None
    label: str | None


@_dataclass
class ContactName:
    nickname: str | None
    given: str | None
    family: str | None
    prefix: str | None
    suffix: str | None
    middle: str | None


@_dataclass
class ContactPhone:
    value: str | None
    type: str | None
    label: str | None


@_dataclass
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


@_dataclass
class EditMessage:
    targetSentTimestamp: int
    dataMessage: DataMessage | None


@_dataclass
class Error:
    message: str | None
    type: str | None


@_dataclass
class GroupInfo:
    groupId: str | None
    groupName: str | None
    revision: int
    type: str | None


@_dataclass
class Mention:
    name: str | None
    number: str | None
    uuid: str | None
    start: int
    length: int


@_dataclass
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


@_dataclass
class Payment:
    note: str | None
    receipt: bytes


@_dataclass
class Preview:
    url: str | None
    title: str | None
    description: str | None
    image: Attachment | None


@_dataclass
class Quote:
    id: int
    author: str | None
    authorNumber: str | None
    authorUuid: str | None
    text: str | None
    mentions: tuple[Mention | None, ...] = ()
    attachments: tuple[QuotedAttachment | None, ...]
    textStyles: tuple[TextStyle | None, ...] = ()


@_dataclass
class QuotedAttachment:
    contentType: str | None
    filename: str | None
    thumbnail: Attachment | None = None


@_dataclass
class Reaction:
    emoji: str | None
    targetAuthor: str | None
    targetAuthorNumber: str | None
    targetAuthorUuid: str | None
    targetSentTimestamp: int
    isRemove: bool


@_dataclass
class ReceiptMessage:
    when: int
    isDelivery: bool
    isRead: bool
    isViewed: bool
    timestamps: tuple[int | None, ...]


@_dataclass
class RecipientAddress:
    uuid: str | None
    number: str | None
    username: str | None


@_dataclass
class RemoteDelete:
    timestamp: int


@_dataclass
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


@_dataclass
class SharedContact:
    name: ContactName | None
    avatar: ContactAvatar | None = None
    phone: tuple[ContactPhone | None, ...] = ()
    email: tuple[ContactEmail | None, ...] = ()
    address: tuple[ContactAddress | None, ...] = ()
    organization: str | None


@_dataclass
class Sticker:
    packId: str | None
    stickerId: int


@_dataclass
class StoryContext:
    authorNumber: str | None
    authorUuid: str | None
    sentTimestamp: int


@_dataclass
class StoryMessage:
    allowsReplies: bool
    groupId: str | None = None
    fileAttachment: Attachment | None = None
    textAttachment: TextAttachment | None = None

    @_dataclass
    class TextAttachment:
        text: str | None
        style: str | None = None
        textForegroundColor: str | None = None
        textBackgroundColor: str | None = None
        preview: Preview | None = None
        backgroundGradient: Gradient | None = None
        backgroundColor: str | None = None

        @_dataclass
        class Gradient:
            startColor: str | None
            endColor: str | None
            colors: tuple[str | None, ...]
            positions: tuple[float | None, ...]
            angle: int | None


@_dataclass
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


@_dataclass
class SyncMessage:
    sentMessage: SyncDataMessage | None = None
    sentStoryMessage: SyncStoryMessage | None = None
    blockedNumbers: tuple[str | None, ...] = ()
    blockedGroupIds: tuple[str | None, ...] = ()
    readMessages: tuple[SyncReadMessage | None, ...] = ()
    type: SyncMessageType | None = None


@_dataclass
class SyncReadMessage:
    sender: str | None
    senderNumber: str | None
    senderUuid: str | None
    timestamp: int


@_dataclass
class SyncStoryMessage:
    destinationNumber: str | None
    destinationUuid: str | None
    dataMessage: StoryMessage | None


@_dataclass
class TextStyle:
    style: str | None
    start: int
    length: int


@_dataclass
class TypingMessage:
    action: str | None
    timestamp: int
    groupId: str | None = None
