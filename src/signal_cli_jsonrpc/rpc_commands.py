from dataclasses import MISSING, dataclass, fields
from typing import Literal, overload

from .rpc_command_outputs import (
    Device,
    Empty,
    Identity,
    JoinGroupResult,
    UpdateGroupResult,
    UploadStickerPackResult,
    UserStatus,
)
from .rpc_session import RpcCommand
from .rpc_types import AttachmentData, Contact

type NonEmptyTuple[T] = tuple[T, *tuple[T, ...]]


@dataclass(frozen=True, kw_only=True)
class AddDevice(RpcCommand, rpc_output_type=Empty):
    """
    Link another device to this device. Only works, if this is the primary device.

    :param uri: Specify the uri contained in the QR code shown by the new device.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/AddDeviceCommand.java
    """

    uri: str


@dataclass(frozen=True, kw_only=True)
class AddStickerPack(RpcCommand, rpc_output_type=Empty):
    """
    Install a sticker pack for this account.

    :param uris: Specify the uri of the sticker pack. (e.g.
        https://signal.art/addstickers/#pack_id=XXX&pack_key=XXX)

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/AddStickerPackCommand.java
    """

    uris: NonEmptyTuple[str]


@dataclass(frozen=True, kw_only=True)
class Block(RpcCommand, rpc_output_type=Empty):
    """
    Block the given contacts or groups (no messages will be received)

    :param recipients: Contact number
    :param group_ids: Group ID

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/BlockCommand.java
    """

    recipients: tuple[str, ...] = ()
    group_ids: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class FinishChangeNumber(RpcCommand, rpc_output_type=Empty):
    """
    Verify the new number using the code received via SMS or voice.

    :param number: The new phone number in E164 format.
    :param verification_code: The verification code you received via sms or voice call.
    :param pin: The registration lock PIN, that was set by the user (Optional)

    Source:
    https://github.com/AsamK/signal-cli/blob/a0d5744c4945791eb57436d0f1288b09bd41132a/src/main/java/org/asamk/signal/commands/FinishChangeNumberCommand.java
    """

    number: str
    verification_code: str
    pin: str | None = None


@dataclass(frozen=True, kw_only=True)
class GetAttachment(RpcCommand, rpc_output_type=AttachmentData):
    """
    Retrieve an already downloaded attachment base64 encoded.

    Note:
     - Exactly one of :attr:`recipient` or :attr:`group_id` is required.

    :param id: The ID of the attachment file.
    :param recipient: Sender of the attachment
    :param group_id: Group in which the attachment was received

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/GetAttachmentCommand.java
    """

    id: str
    recipient: str | None = None
    group_id: str | None = None

    @overload
    def __init__(self, *, id: str, recipient: str): ...

    @overload
    def __init__(self, *, id: str, group_id: str): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := ["recipient", "group_id"])):
            case 0:
                raise ValueError(f"One of {args!r} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args!r} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class GetAvatar(RpcCommand, rpc_output_type=AttachmentData):
    """
    Retrieve the avatar of a contact, contact's profile or group base64 encoded.

    Note:
     - Exactly one of :attr:`contact`, :attr:`profile`, or :attr:`group_id` is required.

    :param contact: Get a contact avatar
    :param profile: Get a profile avatar
    :param group_id: Get a group avatar

    Source:
    https://github.com/AsamK/signal-cli/blob/61bc30eb43b0b156bf271815b4510fe1759086f1/src/main/java/org/asamk/signal/commands/GetAvatarCommand.java
    """

    contact: str | None = None
    profile: str | None = None
    group_id: str | None = None

    @overload
    def __init__(self, *, contact: str): ...

    @overload
    def __init__(self, *, profile: str): ...

    @overload
    def __init__(self, *, group_id: str): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := ["contact", "profile", "group_id"])):
            case 0:
                raise ValueError(f"One of {args!r} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args!r} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class GetSticker(RpcCommand, rpc_output_type=AttachmentData):
    """
    Retrieve the sticker of a sticker pack base64 encoded.

    :param pack_id: The ID of the sticker pack.
    :param sticker_id: The ID of the sticker.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/GetStickerCommand.java
    """

    pack_id: str
    sticker_id: int


@dataclass(frozen=True, kw_only=True)
class GetUserStatus(RpcCommand, rpc_output_type=list[UserStatus]):
    """
    Check if the specified phone number/s have been registered

    :param recipients: Phone number
    :param usernames: Specify the recipient username or username link.

    Source:
    https://github.com/AsamK/signal-cli/blob/ca33249170118be0d2fe3e9deed4ad23b34ac875/src/main/java/org/asamk/signal/commands/GetUserStatusCommand.java
    """

    recipients: tuple[str, ...] = ()
    usernames: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class JoinGroup(RpcCommand, rpc_output_type=JoinGroupResult):
    """
    Join a group via an invitation link.

    :param uri: Specify the uri with the group invitation link.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/JoinGroupCommand.java
    """

    uri: str


@dataclass(frozen=True, kw_only=True)
class ListContacts(RpcCommand, rpc_output_type=list[Contact]):
    """
    Show a list of known contacts with names and profiles.

    :param recipients: Specify one ore more phone numbers to show.
    :param all_recipients: Include all known recipients, not only contacts.
    :param blocked: Specify if only blocked or unblocked contacts should be shown
        (default: all contacts)
    :param name: Find contacts with the given contact or profile name.
    :param detailed: List the contacts with more details. If output=json, then this is always set
    :param internal: Include internal information that's normally not user visible

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListContactsCommand.java
    """

    recipients: tuple[str, ...] = ()
    all_recipients: bool = False
    blocked: bool | None = None
    name: str | None = None
    detailed: bool = False
    internal: bool = False


@dataclass(frozen=True, kw_only=True)
class ListDevices(RpcCommand, rpc_output_type=list[Device]):
    """
    Show a list of linked devices.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListDevicesCommand.java
    """


@dataclass(frozen=True, kw_only=True)
class ListGroups(RpcCommand, rpc_output_type=Empty):
    """
    List group information including names, ids, active status, blocked status and members

    :param detailed: List the members and group invite links of each group. If
        output=json, then this is always set
    :param group_ids: Specify one or more group IDs to show.

    Source:
    https://github.com/AsamK/signal-cli/blob/a22af8303a987905a3a6fb5ab78af11a2dc05b58/src/main/java/org/asamk/signal/commands/ListGroupsCommand.java
    """

    detailed: bool = False
    group_ids: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class ListIdentities(RpcCommand, rpc_output_type=list[Identity]):
    """
    List all known identity keys and their trust status, fingerprint and safety number.

    :param number: Only show identity keys for the given phone number.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListIdentitiesCommand.java
    """

    number: str | None = None


@dataclass(frozen=True, kw_only=True)
class ListStickerPacks(RpcCommand, rpc_output_type=Empty):
    """
    Show a list of known sticker packs.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/ListStickerPacksCommand.java
    """


@dataclass(frozen=True, kw_only=True)
class QuitGroup(RpcCommand, rpc_output_type=Empty):
    """
    Send a quit group message to all group members and remove self from member list.

    :param group_id: Specify the recipient group ID.
    :param delete: Delete local group data completely after quitting group.
    :param admins: Specify one or more members to make a group admin, required if
        you're currently the only admin.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/QuitGroupCommand.java
    """

    group_id: str
    delete: bool = False
    admins: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class RemoteDelete(RpcCommand, rpc_output_type=Empty):
    """
    Remotely delete a previously sent message.

    :param target_timestamp: Specify the timestamp of the message to delete.
    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param usernames: Specify the recipient username or username link.
    :param note_to_self:

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/RemoteDeleteCommand.java
    """

    target_timestamp: int
    group_ids: tuple[str, ...] = ()
    recipients: tuple[str, ...] = ()
    usernames: tuple[str, ...] = ()
    note_to_self: bool = False


@dataclass(frozen=True, kw_only=True)
class RemoveContact(RpcCommand, rpc_output_type=Empty):
    """
    Remove the details of a given contact

    Note:
     - :attr:`hide` and :attr:`forget` are mutually exclusive.

    :param recipient: Contact number
    :param hide: Hide the contact in the contact list, but keep the data.
    :param forget: Delete all data associated with this contact, including identity keys and sessions.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/RemoveContactCommand.java
    """

    recipient: str | None = None
    hide: bool = False
    forget: bool = False

    @overload
    def __init__(self, *, recipient: str | None = ...): ...

    @overload
    def __init__(self, *, recipient: str | None = ..., hide: Literal[True]): ...

    @overload
    def __init__(self, *, recipient: str | None = ..., forget: Literal[True]): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := ["hide", "forget"])):
            case 0 | 1:
                pass
            case _:
                raise ValueError(f"Arguments {args!r} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class RemoveDevice(RpcCommand, rpc_output_type=Empty):
    """
    Remove a linked device.

    :param device_id: Specify the device you want to remove. Use listDevices to see the deviceIds.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/RemoveDeviceCommand.java
    """

    device_id: int


@dataclass(frozen=True, kw_only=True)
class RemovePin(RpcCommand, rpc_output_type=Empty):
    """
    Remove the registration lock pin.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/RemovePinCommand.java
    """


@dataclass(frozen=True, kw_only=True)
class Send(RpcCommand, rpc_output_type=Empty):
    """
    Send a message to another user or group.

    :param recipients: Specify the recipients' phone number.
    :param group_ids: Specify the recipient group ID.
    :param usernames: Specify the recipient username or username link.
    :param note_to_self: Send the message to self without notification.
    :param notify_self: If self is part of recipients/groups send a normal message, not a sync message.
    :param message: Specify the message to be sent.
    :param attachments: Add an attachment. Can be either a file path or a data URI. Data URI
        encoded attachments must follow the RFC 2397. Additionally a file name can be added,
        e.g. data:<MIME-TYPE>;filename=<FILENAME>;base64,<BASE64 ENCODED DATA>.
    :param view_once: Send the message as a view once message
    :param end_session: Clear session state and send end session message.
    :param mentions: Mention another group member (syntax:
        start:length:recipientNumber). Unit of start and length is UTF-16 code
        units, NOT Unicode code points.
    :param text_styles: Style parts of the message text (syntax: start:length:STYLE). Unit of
        start and length is UTF-16 code units, NOT Unicode code points.
    :param quote_timestamp: Specify the timestamp of a previous message with the
        recipient or group to add a quote to the new message.
    :param quote_author: Specify the number of the author of the original message.
    :param quote_message: Specify the message of the original message.
    :param quote_mentions: Quote with mention of another group member (syntax:
        start:length:recipientNumber)
    :param quote_attachments: Specify the attachments of the original message
        (syntax: contentType[:filename[:previewFile]]), e.g. 'audio/aac' or
        'image/png:test.png:/tmp/preview.jpg'.
    :param quote_text_styles: Quote with style parts of the message text (syntax: start:length:STYLE)
    :param sticker: Send a sticker (syntax: stickerPackId:stickerId)
    :param preview_url: Specify the url for the link preview (the same url must also
        appear in the message body).
    :param preview_title: Specify the title for the link preview (mandatory).
    :param preview_description: Specify the description for the link preview (optional).
    :param preview_image: Specify the image file for the link preview (optional).
    :param story_timestamp: Specify the timestamp of a story to reply to.
    :param story_author: Specify the number of the author of the story.
    :param edit_timestamp: Specify the timestamp of a previous message with the
        recipient or group to send an edited message.

    Source:
    https://github.com/AsamK/signal-cli/blob/3e981d66e9534db61953078b3ca8faf16ed9dd2d/src/main/java/org/asamk/signal/commands/SendCommand.java
    """

    recipients: tuple[str, ...] = ()
    group_ids: tuple[str, ...] = ()
    usernames: tuple[str, ...] = ()
    note_to_self: bool = False
    notify_self: bool = False
    message: str | None = None
    attachments: tuple[str, ...] = ()
    view_once: bool = False
    end_session: bool = False
    mentions: tuple[str, ...] = ()
    text_styles: tuple[str, ...] = ()
    quote_timestamp: int | None = None
    quote_author: str | None = None
    quote_message: str | None = None
    quote_mentions: tuple[str, ...] = ()
    quote_attachments: tuple[str, ...] = ()
    quote_text_styles: tuple[str, ...] = ()
    sticker: str | None = None
    preview_url: str | None = None
    preview_title: str | None = None
    preview_description: str | None = None
    preview_image: str | None = None
    story_timestamp: int | None = None
    story_author: str | None = None
    edit_timestamp: int | None = None


@dataclass(frozen=True, kw_only=True)
class SendContacts(RpcCommand, rpc_output_type=Empty):
    """
    Send a synchronization message with the local contacts list to all linked devices.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SendContactsCommand.java
    """


@dataclass(frozen=True, kw_only=True)
class SendMessageRequestResponse(RpcCommand, rpc_output_type=Empty):
    """
    Send response to a message request to linked devices.

    :param type: Type of message request response
    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param usernames: Specify the recipient username or username link.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SendMessageRequestResponseCommand.java
    """

    type: Literal[("accept", "delete")]
    group_ids: tuple[str, ...] = ()
    recipients: tuple[str, ...] = ()
    usernames: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class SendPaymentNotification(RpcCommand, rpc_output_type=Empty):
    """
    Send a payment notification.

    :param receipt: The base64 encoded receipt blob.
    :param recipient: Specify the recipient's phone number.
    :param note: Specify a note for the payment notification.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SendPaymentNotificationCommand.java
    """

    receipt: str
    recipient: str | None = None
    note: str | None = None


@dataclass(frozen=True, kw_only=True)
class SendReaction(RpcCommand, rpc_output_type=Empty):
    """
    Send reaction to a previously received or sent message.

    :param emoji: Specify the emoji, should be a single unicode grapheme cluster.
    :param target_author: Specify the number of the author of the message to which to react.
    :param target_timestamp: Specify the timestamp of the message to which to react.
    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param usernames: Specify the recipient username or username link.
    :param note_to_self: Send the reaction to self without notification.
    :param remove: Remove a reaction.
    :param story: React to a story instead of a normal message

    Source:
    https://github.com/AsamK/signal-cli/blob/fe752e0c7998bc8ca66c46d981624e6fbce7abf9/src/main/java/org/asamk/signal/commands/SendReactionCommand.java
    """

    emoji: str
    target_author: str
    target_timestamp: int
    group_ids: tuple[str, ...] = ()
    recipients: tuple[str, ...] = ()
    usernames: tuple[str, ...] = ()
    note_to_self: bool = False
    remove: bool = False
    story: bool = False


@dataclass(frozen=True, kw_only=True)
class SendReceipt(RpcCommand, rpc_output_type=Empty):
    """
    Send a read or viewed receipt to a previously received message.

    :param recipient: Specify the sender's phone number.
    :param target_timestamps: Specify the timestamp of the messages for which a
        receipt should be sent.
    :param type: Specify the receipt type (default is read receipt).

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SendReceiptCommand.java
    """

    recipient: str
    target_timestamps: NonEmptyTuple[int]
    type: Literal[("read", "viewed")] | None = None


@dataclass(frozen=True, kw_only=True)
class SendSyncRequest(RpcCommand, rpc_output_type=Empty):
    """
    Send a synchronization request message to primary device (for group, contacts, ...).

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SendSyncRequestCommand.java
    """


@dataclass(frozen=True, kw_only=True)
class SendTyping(RpcCommand, rpc_output_type=Empty):
    """
    Send typing message to trigger a typing indicator for the recipient. Indicator
    will be shown for 15seconds unless a typing STOP message is sent first.

    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param stop: Send a typing STOP message.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SendTypingCommand.java
    """

    group_ids: tuple[str, ...] = ()
    recipients: tuple[str, ...] = ()
    stop: bool = False


@dataclass(frozen=True, kw_only=True)
class SetPin(RpcCommand, rpc_output_type=Empty):
    """
    Set a registration lock pin, to prevent others from registering this number.

    :param pin: The registration lock PIN, that will be required for new
        registrations (resets after 7 days of inactivity)

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/SetPinCommand.java
    """

    pin: str | None = None


@dataclass(frozen=True, kw_only=True)
class StartChangeNumber(RpcCommand, rpc_output_type=Empty):
    """
    Change account to a new phone number with SMS or voice verification.

    :param number: The new phone number in E164 format.
    :param voice: The verification should be done over voice, not SMS.
    :param captcha: The captcha token, required if change number failed with a
        captcha required error.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/StartChangeNumberCommand.java
    """

    number: str
    voice: bool = False
    captcha: str | None = None


@dataclass(frozen=True, kw_only=True)
class SubmitRateLimitChallenge(RpcCommand, rpc_output_type=Empty):
    """
    Submit a captcha challenge to lift the rate limit. This command should only be
    necessary when sending fails with a proof required error.

    :param challenge: The challenge token taken from the proof required error.
    :param captcha: The captcha token from the solved captcha on the signal website.

    Source:
    https://github.com/AsamK/signal-cli/blob/189b21dbde0b9981365ee6e39e3645b94d634ef6/src/main/java/org/asamk/signal/commands/SubmitRateLimitChallengeCommand.java
    """

    challenge: str
    captcha: str


@dataclass(frozen=True, kw_only=True)
class Trust(RpcCommand, rpc_output_type=Empty):
    """
    Set the trust level of a given number.

    Note:
     - :attr:`trust_all_known_keys` and :attr:`verified_safety_number` are mutually exclusive.

    :param recipient: Specify the phone number, for which to set the trust.
    :param trust_all_known_keys: Trust all known keys of this user, only use this for testing.
    :param verified_safety_number: Specify the safety number of the key, only use
        this option if you have verified the safety number.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/TrustCommand.java
    """

    recipient: str
    trust_all_known_keys: bool = False
    verified_safety_number: str | None = None

    @overload
    def __init__(self, *, recipient: str): ...

    @overload
    def __init__(self, *, recipient: str, trust_all_known_keys: Literal[True]): ...

    @overload
    def __init__(self, *, recipient: str, verified_safety_number: str): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := ["trust_all_known_keys", "verified_safety_number"])):
            case 0 | 1:
                pass
            case _:
                raise ValueError(f"Arguments {args!r} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class Unblock(RpcCommand, rpc_output_type=Empty):
    """
    Unblock the given contacts or groups (messages will be received again)

    :param recipients: Contact number
    :param group_ids: Group ID

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UnblockCommand.java
    """

    recipients: tuple[str, ...] = ()
    group_ids: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class Unregister(RpcCommand, rpc_output_type=Empty):
    """
    Unregister the current device from the signal server.

    :param delete_account: Delete account completely from server. CAUTION: Only do
        this if you won't use this number again!

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UnregisterCommand.java
    """

    delete_account: bool = False


@dataclass(frozen=True, kw_only=True)
class UpdateAccount(RpcCommand, rpc_output_type=Empty):
    """
    Update the account attributes on the signal server.

    Note:
     - :attr:`username` and :attr:`delete_username` are mutually exclusive.

    :param device_name: Specify a name to describe this device.
    :param unrestricted_unidentified_sender: Enable if anyone should be able to send
        you unidentified sender messages.
    :param discoverable_by_number: Enable/disable if the account should be
        discoverable by phone number
    :param number_sharing: Indicates if Signal should share its phone number when sending a message.
    :param username: Specify a username that can then be used to contact this account.
    :param delete_username: Delete the username associated with this account.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UpdateAccountCommand.java
    """

    device_name: str | None = None
    unrestricted_unidentified_sender: bool | None = None
    discoverable_by_number: bool | None = None
    number_sharing: bool | None = None
    username: str | None = None
    delete_username: bool = False

    @overload
    def __init__(
        self,
        *,
        device_name: str | None = ...,
        unrestricted_unidentified_sender: bool | None = ...,
        discoverable_by_number: bool | None = ...,
        number_sharing: bool | None = ...,
    ): ...

    @overload
    def __init__(
        self,
        *,
        device_name: str | None = ...,
        unrestricted_unidentified_sender: bool | None = ...,
        discoverable_by_number: bool | None = ...,
        number_sharing: bool | None = ...,
        username: str,
    ): ...

    @overload
    def __init__(
        self,
        *,
        device_name: str | None = ...,
        unrestricted_unidentified_sender: bool | None = ...,
        discoverable_by_number: bool | None = ...,
        number_sharing: bool | None = ...,
        delete_username: Literal[True],
    ): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := ["username", "delete_username"])):
            case 0 | 1:
                pass
            case _:
                raise ValueError(f"Arguments {args!r} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class UpdateConfiguration(RpcCommand, rpc_output_type=Empty):
    """
    Update signal configs and sync them to linked devices.

    :param read_receipts: Indicates if Signal should send read receipts.
    :param unidentified_delivery_indicators: Indicates if Signal should show
        unidentified delivery indicators.
    :param typing_indicators: Indicates if Signal should send/show typing indicators.
    :param link_previews: Indicates if Signal should generate link previews.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UpdateConfigurationCommand.java
    """

    read_receipts: bool | None = None
    unidentified_delivery_indicators: bool | None = None
    typing_indicators: bool | None = None
    link_previews: bool | None = None


@dataclass(frozen=True, kw_only=True)
class UpdateContact(RpcCommand, rpc_output_type=Empty):
    """
    Update the details of a given contact

    :param recipient: Contact number
    :param name: New contact name
    :param given_name: New system given name
    :param family_name: New system family name
    :param nick_given_name: New nick given name
    :param nick_family_name: New nick family name
    :param note: New note
    :param expiration: Set expiration time of messages (seconds)

    Source:
    https://github.com/AsamK/signal-cli/blob/1af03e3e16d77820d64e034e926795e4cb6f7c8a/src/main/java/org/asamk/signal/commands/UpdateContactCommand.java
    """

    recipient: str | None = None
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    nick_given_name: str | None = None
    nick_family_name: str | None = None
    note: str | None = None
    expiration: int | None = None


@dataclass(frozen=True, kw_only=True)
class UpdateGroup(RpcCommand, rpc_output_type=UpdateGroupResult):
    """
    Create or update a group.

    :param group_id: Specify the group ID.
    :param name: Specify the new group name.
    :param description: Specify the new group description.
    :param avatar: Specify a new group avatar image file
    :param members: Specify one or more members to add to the group
    :param remove_members: Specify one or more members to remove from the group
    :param admins: Specify one or more members to make a group admin
    :param remove_admins: Specify one or more members to remove group admin privileges
    :param bans: Specify one or more members to ban from joining the group
    :param unbans: Specify one or more members to remove from the ban list
    :param reset_link: Reset group link and create new link password
    :param link: Set group link state, with or without admin approval
    :param set_permission_add_member: Set permission to add new group members
    :param set_permission_edit_details: Set permission to edit group details
    :param set_permission_send_messages: Set permission to send messages
    :param expiration: Set expiration time of messages (seconds)

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UpdateGroupCommand.java
    """

    group_id: str | None = None
    name: str | None = None
    description: str | None = None
    avatar: str | None = None
    members: tuple[str, ...] = ()
    remove_members: tuple[str, ...] = ()
    admins: tuple[str, ...] = ()
    remove_admins: tuple[str, ...] = ()
    bans: tuple[str, ...] = ()
    unbans: tuple[str, ...] = ()
    reset_link: bool = False
    link: Literal[("enabled", "enabled-with-approval", "disabled")] | None = None
    set_permission_add_member: Literal[("every-member", "only-admins")] | None = None
    set_permission_edit_details: Literal[("every-member", "only-admins")] | None = None
    set_permission_send_messages: Literal[("every-member", "only-admins")] | None = None
    expiration: int | None = None


@dataclass(frozen=True, kw_only=True)
class UpdateProfile(RpcCommand, rpc_output_type=Empty):
    """
    Set a name, about and avatar image for the user profile

    Note:
     - :attr:`avatar` and :attr:`remove_avatar` are mutually exclusive.

    :param given_name: New profile (given) name
    :param family_name: New profile family name (optional)
    :param about: New profile about text
    :param about_emoji: New profile about emoji
    :param mobile_coin_address: New MobileCoin address (Base64 encoded public address)
    :param avatar: Path to new profile avatar
    :param remove_avatar:

    Source:
    https://github.com/AsamK/signal-cli/blob/a6ec71dc315e5b259a7bfe70cad46b7780b73fa9/src/main/java/org/asamk/signal/commands/UpdateProfileCommand.java
    """

    given_name: str | None = None
    family_name: str | None = None
    about: str | None = None
    about_emoji: str | None = None
    mobile_coin_address: str | None = None
    avatar: str | None = None
    remove_avatar: bool = False

    @overload
    def __init__(
        self,
        *,
        given_name: str | None = ...,
        family_name: str | None = ...,
        about: str | None = ...,
        about_emoji: str | None = ...,
        mobile_coin_address: str | None = ...,
    ): ...

    @overload
    def __init__(
        self,
        *,
        given_name: str | None = ...,
        family_name: str | None = ...,
        about: str | None = ...,
        about_emoji: str | None = ...,
        mobile_coin_address: str | None = ...,
        avatar: str,
    ): ...

    @overload
    def __init__(
        self,
        *,
        given_name: str | None = ...,
        family_name: str | None = ...,
        about: str | None = ...,
        about_emoji: str | None = ...,
        mobile_coin_address: str | None = ...,
        remove_avatar: Literal[True],
    ): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := ["avatar", "remove_avatar"])):
            case 0 | 1:
                pass
            case _:
                raise ValueError(f"Arguments {args!r} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class UploadStickerPack(RpcCommand, rpc_output_type=UploadStickerPackResult):
    """
    Upload a new sticker pack, consisting of a manifest file and the stickers images.

    :param path: The path of the manifest.json or a zip file containing the sticker
        pack you wish to upload.

    Source:
    https://github.com/AsamK/signal-cli/blob/f2005593ecefd37c7e1666c2dc0c71b259271af0/src/main/java/org/asamk/signal/commands/UploadStickerPackCommand.java
    """

    path: str | None = None
