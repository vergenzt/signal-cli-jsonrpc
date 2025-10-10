from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional


@dataclass
class Attachment:
    contentType: Optional[str]
    filename: Optional[str]
    id: Optional[str]
    size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    caption: Optional[str]
    uploadTimestamp: Optional[int]


@dataclass
class AttachmentData:
    data: Optional[str]


@dataclass
class CallMessage:
    offerMessage: Offer
    answerMessage: Answer
    busyMessage: Busy
    hangupMessage: Hangup
    iceUpdateMessages: list[IceUpdate]

    @dataclass
    class Offer:
        id: int
        type: Optional[str]
        opaque: Optional[str]

    @dataclass
    class Answer:
        id: int
        opaque: Optional[str]

    @dataclass
    class Busy:
        id: int

    @dataclass
    class Hangup:
        id: int
        type: Optional[str]
        deviceId: int

    @dataclass
    class IceUpdate:
        id: int
        opaque: Optional[str]


@dataclass
class Contact:
    number: Optional[str]
    uuid: Optional[str]
    username: Optional[str]
    name: Optional[str]
    givenName: Optional[str]
    familyName: Optional[str]
    nickName: Optional[str]
    nickGivenName: Optional[str]
    nickFamilyName: Optional[str]
    note: Optional[str]
    color: Optional[str]
    isBlocked: bool
    isHidden: bool
    messageExpirationTime: int
    profileSharing: bool
    unregistered: bool
    profile: Profile
    internal: Internal

    @dataclass
    class Profile:
        lastUpdateTimestamp: int
        givenName: Optional[str]
        familyName: Optional[str]
        about: Optional[str]
        aboutEmoji: Optional[str]
        hasAvatar: bool
        mobileCoinAddress: Optional[str]

    @dataclass
    class Internal:
        capabilities: list[Optional[str]]
        unidentifiedAccessMode: Optional[str]
        sharesPhoneNumber: bool
        discoverableByPhonenumber: bool


@dataclass
class ContactAddress:
    type: Optional[str]
    label: Optional[str]
    street: Optional[str]
    pobox: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    region: Optional[str]
    postcode: Optional[str]
    country: Optional[str]


@dataclass
class ContactAvatar:
    attachment: Attachment
    isProfile: bool


@dataclass
class ContactEmail:
    value: Optional[str]
    type: Optional[str]
    label: Optional[str]


@dataclass
class ContactName:
    nickname: Optional[str]
    given: Optional[str]
    family: Optional[str]
    prefix: Optional[str]
    suffix: Optional[str]
    middle: Optional[str]


@dataclass
class ContactPhone:
    value: Optional[str]
    type: Optional[str]
    label: Optional[str]


@dataclass
class DataMessage:
    timestamp: int
    message: Optional[str]
    expiresInSeconds: Optional[int]
    viewOnce: bool
    reaction: Reaction
    quote: Quote
    payment: Payment
    mentions: list[Mention]
    previews: list[Preview]
    attachments: list[Attachment]
    sticker: Sticker
    remoteDelete: RemoteDelete
    contacts: list[SharedContact]
    textStyles: list[TextStyle]
    groupInfo: GroupInfo
    storyContext: StoryContext


@dataclass
class EditMessage:
    targetSentTimestamp: int
    dataMessage: DataMessage


@dataclass
class Error:
    message: Optional[str]
    type: Optional[str]


@dataclass
class GroupInfo:
    groupId: Optional[str]
    groupName: Optional[str]
    revision: int
    type: Optional[str]


@dataclass
class Mention:
    name: Optional[str]
    number: Optional[str]
    uuid: Optional[str]
    start: int
    length: int


@dataclass
class MessageEnvelope:
    source: Optional[str]
    sourceNumber: Optional[str]
    sourceUuid: Optional[str]
    sourceName: Optional[str]
    sourceDevice: Optional[int]
    timestamp: int
    serverReceivedTimestamp: int
    serverDeliveredTimestamp: int
    dataMessage: DataMessage
    editMessage: EditMessage
    storyMessage: StoryMessage
    syncMessage: SyncMessage
    callMessage: CallMessage
    receiptMessage: ReceiptMessage
    typingMessage: TypingMessage


@dataclass
class Payment:
    note: Optional[str]
    receipt: bytes


@dataclass
class Preview:
    url: Optional[str]
    title: Optional[str]
    description: Optional[str]
    image: Attachment


@dataclass
class Quote:
    id: int
    author: Optional[str]
    authorNumber: Optional[str]
    authorUuid: Optional[str]
    text: Optional[str]
    mentions: list[Mention]
    attachments: list[QuotedAttachment]
    textStyles: list[TextStyle]


@dataclass
class QuotedAttachment:
    contentType: Optional[str]
    filename: Optional[str]
    thumbnail: Attachment


@dataclass
class Reaction:
    emoji: Optional[str]
    targetAuthor: Optional[str]
    targetAuthorNumber: Optional[str]
    targetAuthorUuid: Optional[str]
    targetSentTimestamp: int
    isRemove: bool


@dataclass
class ReceiptMessage:
    when: int
    isDelivery: bool
    isRead: bool
    isViewed: bool
    timestamps: list[Optional[int]]


@dataclass
class RecipientAddress:
    uuid: Optional[str]
    number: Optional[str]
    username: Optional[str]


@dataclass
class RemoteDelete:
    timestamp: int


@dataclass
class SendMessageResult:
    recipientAddress: RecipientAddress
    groupId: Optional[str]
    type: Type
    token: Optional[str]
    retryAfterSeconds: Optional[int]

    class Type(StrEnum):
        SUCCESS = auto()
        NETWORK_FAILURE = auto()
        UNREGISTERED_FAILURE = auto()
        IDENTITY_FAILURE = auto()
        RATE_LIMIT_FAILURE = auto()
        INVALID_PRE_KEY_FAILURE = auto()


@dataclass
class SharedContact:
    name: ContactName
    avatar: ContactAvatar
    phone: list[ContactPhone]
    email: list[ContactEmail]
    address: list[ContactAddress]
    organization: Optional[str]


@dataclass
class Sticker:
    packId: Optional[str]
    stickerId: int


@dataclass
class StoryContext:
    authorNumber: Optional[str]
    authorUuid: Optional[str]
    sentTimestamp: int


@dataclass
class StoryMessage:
    allowsReplies: bool
    groupId: Optional[str]
    fileAttachment: Attachment
    textAttachment: TextAttachment

    @dataclass
    class TextAttachment:
        text: Optional[str]
        style: Optional[str]
        textForegroundColor: Optional[str]
        textBackgroundColor: Optional[str]
        preview: Preview
        backgroundGradient: Gradient
        backgroundColor: Optional[str]

        @dataclass
        class Gradient:
            startColor: Optional[str]
            endColor: Optional[str]
            colors: list[Optional[str]]
            positions: list[float]
            angle: Optional[int]


@dataclass
class SyncDataMessage:
    destination: Optional[str]
    destinationNumber: Optional[str]
    destinationUuid: Optional[str]
    editMessage: EditMessage
    dataMessage: DataMessage


class SyncMessageType(StrEnum):
    CONTACTS_SYNC = auto()
    GROUPS_SYNC = auto()
    REQUEST_SYNC = auto()


@dataclass
class SyncMessage:
    sentMessage: SyncDataMessage
    sentStoryMessage: SyncStoryMessage
    blockedNumbers: list[Optional[str]]
    blockedGroupIds: list[Optional[str]]
    readMessages: list[SyncReadMessage]
    type: SyncMessageType


@dataclass
class SyncReadMessage:
    sender: Optional[str]
    senderNumber: Optional[str]
    senderUuid: Optional[str]
    timestamp: int


@dataclass
class SyncStoryMessage:
    destinationNumber: Optional[str]
    destinationUuid: Optional[str]
    dataMessage: StoryMessage


@dataclass
class TextStyle:
    style: Optional[str]
    start: int
    length: int


@dataclass
class TypingMessage:
    action: Optional[str]
    timestamp: int
    groupId: Optional[str]
