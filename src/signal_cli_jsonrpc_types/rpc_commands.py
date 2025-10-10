from dataclasses import MISSING, dataclass, fields
from typing import Literal, Optional, overload

from . import Contact
from .rpc_session import Empty, RpcCommand

type NonEmptyTuple[T] = tuple[T, *tuple[T, ...]]


@dataclass(frozen=True, kw_only=True)
class AddDevice(RpcCommand, rpc_output_type=Empty):
    """
    Link another device to this device. Only works, if this is the primary device.

    :param uri: Specify the uri contained in the QR code shown by the new device.
    """

    uri: str
    "Specify the uri contained in the QR code shown by the new device."


@dataclass(frozen=True, kw_only=True)
class AddStickerPack(RpcCommand, rpc_output_type=Empty):
    """
    Install a sticker pack for this account.

    :param uris: Specify the uri of the sticker pack. (e.g.
        https://signal.art/addstickers/#pack_id=XXX&pack_key=XXX)
    """

    uris: NonEmptyTuple[str]
    """
    Specify the uri of the sticker pack. (e.g.
    https://signal.art/addstickers/#pack_id=XXX&pack_key=XXX)
    """


@dataclass(frozen=True, kw_only=True)
class Block(RpcCommand):
    """
    Block the given contacts or groups (no messages will be received)

    :param recipients: Contact number
    :param group_ids: Group ID
    """

    recipients: tuple[str, ...] = ()
    "Contact number"
    group_ids: tuple[str, ...] = ()
    "Group ID"


@dataclass(frozen=True, kw_only=True)
class FinishChangeNumber(RpcCommand):
    """
    Verify the new number using the code received via SMS or voice.

    :param number: The new phone number in E164 format.
    :param verification_code: The verification code you received via sms or voice call.
    :param pin: The registration lock PIN, that was set by the user (Optional)
    """

    number: str
    "The new phone number in E164 format."
    verification_code: str
    "The verification code you received via sms or voice call."
    pin: Optional[str] = None
    "The registration lock PIN, that was set by the user (Optional)"


@dataclass(frozen=True, kw_only=True)
class GetAttachment(RpcCommand):
    """
    Retrieve an already downloaded attachment base64 encoded.

    :param id: The ID of the attachment file.
    :param recipient: Sender of the attachment
    :param group_id: Group in which the attachment was received
    """

    id: str
    "The ID of the attachment file."
    recipient: Optional[str] = None
    "Sender of the attachment"
    group_id: Optional[str] = None
    "Group in which the attachment was received"

    @overload
    def __init__(self, *, id: str, recipient: str): ...

    @overload
    def __init__(self, *, id: str, group_id: str): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := {"recipient", "group_id"})):
            case 0:
                raise ValueError(f"One of {args} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class GetAvatar(RpcCommand):
    """
    Retrieve the avatar of a contact, contact's profile or group base64 encoded.

    :param contact: Get a contact avatar
    :param profile: Get a profile avatar
    :param group_id: Get a group avatar
    """

    contact: Optional[str] = None
    "Get a contact avatar"
    profile: Optional[str] = None
    "Get a profile avatar"
    group_id: Optional[str] = None
    "Get a group avatar"

    @overload
    def __init__(self, *, contact: str): ...

    @overload
    def __init__(self, *, profile: str): ...

    @overload
    def __init__(self, *, group_id: str): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := {"contact", "profile", "group_id"})):
            case 0:
                raise ValueError(f"One of {args} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class GetSticker(RpcCommand):
    """
    Retrieve the sticker of a sticker pack base64 encoded.

    :param pack_id: The ID of the sticker pack.
    :param sticker_id: The ID of the sticker.
    """

    pack_id: str
    "The ID of the sticker pack."
    sticker_id: int
    "The ID of the sticker."


@dataclass(frozen=True, kw_only=True)
class GetUserStatus(RpcCommand):
    """
    Check if the specified phone number/s have been registered

    :param recipients: Phone number
    :param usernames: Specify the recipient username or username link.
    """

    recipients: tuple[str, ...] = ()
    "Phone number"
    usernames: tuple[str, ...] = ()
    "Specify the recipient username or username link."


@dataclass(frozen=True, kw_only=True)
class JoinGroup(RpcCommand):
    """
    Join a group via an invitation link.

    :param uri: Specify the uri with the group invitation link.
    """

    uri: str
    "Specify the uri with the group invitation link."


@dataclass(frozen=True, kw_only=True)
class ListContacts(RpcCommand, rpc_result_type=list[Contact]):
    """
    Show a list of known contacts with names and profiles.

    :param blocked: Specify if only blocked or unblocked contacts should be shown
        (default: all contacts)
    :param name: Find contacts with the given contact or profile name.
    :param recipients: Specify one ore more phone numbers to show.
    :param all_recipients: Include all known recipients, not only contacts.
    :param detailed: List the contacts with more details. If output=json, then this is always set
    :param internal: Include internal information that's normally not user visible
    """

    blocked: Optional[bool] = None
    "Specify if only blocked or unblocked contacts should be shown (default: all contacts)"
    name: Optional[str] = None
    "Find contacts with the given contact or profile name."
    recipients: tuple[str, ...] = ()
    "Specify one ore more phone numbers to show."
    all_recipients: bool = False
    "Include all known recipients, not only contacts."
    detailed: bool = False
    "List the contacts with more details. If output=json, then this is always set"
    internal: bool = False
    "Include internal information that's normally not user visible"


@dataclass(frozen=True, kw_only=True)
class ListDevices(RpcCommand):
    "Show a list of linked devices."


@dataclass(frozen=True, kw_only=True)
class ListGroups(RpcCommand):
    """
    List group information including names, ids, active status, blocked status and members

    :param detailed: List the members and group invite links of each group. If
        output=json, then this is always set
    :param group_ids: Specify one or more group IDs to show.
    """

    detailed: bool = False
    "List the members and group invite links of each group. If output=json, then this is always set"
    group_ids: tuple[str, ...] = ()
    "Specify one or more group IDs to show."


@dataclass(frozen=True, kw_only=True)
class ListIdentities(RpcCommand):
    """
    List all known identity keys and their trust status, fingerprint and safety number.

    :param number: Only show identity keys for the given phone number.
    """

    number: Optional[str] = None
    "Only show identity keys for the given phone number."


@dataclass(frozen=True, kw_only=True)
class ListStickerPacks(RpcCommand):
    "Show a list of known sticker packs."


@dataclass(frozen=True, kw_only=True)
class QuitGroup(RpcCommand):
    """
    Send a quit group message to all group members and remove self from member list.

    :param group_id: Specify the recipient group ID.
    :param delete: Delete local group data completely after quitting group.
    :param admins: Specify one or more members to make a group admin, required if
        you're currently the only admin.
    """

    group_id: str
    "Specify the recipient group ID."
    delete: bool = False
    "Delete local group data completely after quitting group."
    admins: tuple[str, ...] = ()
    "Specify one or more members to make a group admin, required if you're currently the only admin."


@dataclass(frozen=True, kw_only=True)
class RemoteDelete(RpcCommand):
    """
    Remotely delete a previously sent message.

    :param target_timestamp: Specify the timestamp of the message to delete.
    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param usernames: Specify the recipient username or username link.
    :param note_to_self: None
    """

    target_timestamp: int
    "Specify the timestamp of the message to delete."
    group_ids: tuple[str, ...] = ()
    "Specify the recipient group ID."
    recipients: tuple[str, ...] = ()
    "Specify the recipients' phone number."
    usernames: tuple[str, ...] = ()
    "Specify the recipient username or username link."
    note_to_self: bool = False


@dataclass(frozen=True, kw_only=True)
class RemoveContact(RpcCommand):
    """
    Remove the details of a given contact

    :param recipient: Contact number
    :param hide: Hide the contact in the contact list, but keep the data.
    :param forget: Delete all data associated with this contact, including identity keys and sessions.
    """

    recipient: Optional[str] = None
    "Contact number"
    hide: bool = False
    "Hide the contact in the contact list, but keep the data."
    forget: bool = False
    "Delete all data associated with this contact, including identity keys and sessions."

    @overload
    def __init__(self, *, recipient: Optional[str] = None): ...

    @overload
    def __init__(self, *, recipient: Optional[str] = None, hide: Literal[True]): ...

    @overload
    def __init__(self, *, recipient: Optional[str] = None, forget: Literal[True]): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := {"hide", "forget"})):
            case 0:
                raise ValueError(f"One of {args} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class RemoveDevice(RpcCommand):
    """
    Remove a linked device.

    :param device_id: Specify the device you want to remove. Use listDevices to see the deviceIds.
    """

    device_id: int
    "Specify the device you want to remove. Use listDevices to see the deviceIds."


@dataclass(frozen=True, kw_only=True)
class RemovePin(RpcCommand):
    "Remove the registration lock pin."


@dataclass(frozen=True, kw_only=True)
class Send(RpcCommand):
    """
    Send a message to another user or group.

    :param message: Specify the message to be sent.
    :param quote_timestamp: Specify the timestamp of a previous message with the
        recipient or group to add a quote to the new message.
    :param quote_author: Specify the number of the author of the original message.
    :param quote_message: Specify the message of the original message.
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
    :param recipients: Specify the recipients' phone number.
    :param group_ids: Specify the recipient group ID.
    :param usernames: Specify the recipient username or username link.
    :param note_to_self: Send the message to self without notification.
    :param notify_self: If self is part of recipients/groups send a normal message, not a sync message.
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
    :param quote_mentions: Quote with mention of another group member (syntax:
        start:length:recipientNumber)
    :param quote_attachments: Specify the attachments of the original message
        (syntax: contentType[:filename[:previewFile]]), e.g. 'audio/aac' or
        'image/png:test.png:/tmp/preview.jpg'.
    :param quote_text_styles: Quote with style parts of the message text (syntax: start:length:STYLE)
    """

    message: Optional[str] = None
    "Specify the message to be sent."
    quote_timestamp: Optional[int] = None
    """
    Specify the timestamp of a previous message with the recipient or
    group to add a quote to the new message.
    """
    quote_author: Optional[str] = None
    "Specify the number of the author of the original message."
    quote_message: Optional[str] = None
    "Specify the message of the original message."
    sticker: Optional[str] = None
    "Send a sticker (syntax: stickerPackId:stickerId)"
    preview_url: Optional[str] = None
    "Specify the url for the link preview (the same url must also appear in the message body)."
    preview_title: Optional[str] = None
    "Specify the title for the link preview (mandatory)."
    preview_description: Optional[str] = None
    "Specify the description for the link preview (optional)."
    preview_image: Optional[str] = None
    "Specify the image file for the link preview (optional)."
    story_timestamp: Optional[int] = None
    "Specify the timestamp of a story to reply to."
    story_author: Optional[str] = None
    "Specify the number of the author of the story."
    edit_timestamp: Optional[int] = None
    "Specify the timestamp of a previous message with the recipient or group to send an edited message."
    recipients: tuple[str, ...] = ()
    "Specify the recipients' phone number."
    group_ids: tuple[str, ...] = ()
    "Specify the recipient group ID."
    usernames: tuple[str, ...] = ()
    "Specify the recipient username or username link."
    note_to_self: bool = False
    "Send the message to self without notification."
    notify_self: bool = False
    "If self is part of recipients/groups send a normal message, not a sync message."
    attachments: tuple[str, ...] = ()
    """
    Add an attachment. Can be either a file path or a data URI. Data URI encoded
    attachments must follow the RFC 2397. Additionally a file name can be added,
    e.g. data:<MIME-TYPE>;filename=<FILENAME>;base64,<BASE64 ENCODED DATA>.
    """
    view_once: bool = False
    "Send the message as a view once message"
    end_session: bool = False
    "Clear session state and send end session message."
    mentions: tuple[str, ...] = ()
    """
    Mention another group member (syntax: start:length:recipientNumber). Unit of
    start and length is UTF-16 code units, NOT Unicode code points.
    """
    text_styles: tuple[str, ...] = ()
    """
    Style parts of the message text (syntax: start:length:STYLE). Unit of start and
    length is UTF-16 code units, NOT Unicode code points.
    """
    quote_mentions: tuple[str, ...] = ()
    """
    Quote with mention of another group member (syntax:
    start:length:recipientNumber)
    """
    quote_attachments: tuple[str, ...] = ()
    """
    Specify the attachments of the original message (syntax:
    contentType[:filename[:previewFile]]), e.g. 'audio/aac' or
    'image/png:test.png:/tmp/preview.jpg'.
    """
    quote_text_styles: tuple[str, ...] = ()
    "Quote with style parts of the message text (syntax: start:length:STYLE)"


@dataclass(frozen=True, kw_only=True)
class SendContacts(RpcCommand):
    "Send a synchronization message with the local contacts list to all linked devices."


@dataclass(frozen=True, kw_only=True)
class SendMessageRequestResponse(RpcCommand):
    """
    Send response to a message request to linked devices.

    :param type: Type of message request response
    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param usernames: Specify the recipient username or username link.
    """

    type: Literal["accept", "delete"]
    "Type of message request response"
    group_ids: tuple[str, ...] = ()
    "Specify the recipient group ID."
    recipients: tuple[str, ...] = ()
    "Specify the recipients' phone number."
    usernames: tuple[str, ...] = ()
    "Specify the recipient username or username link."


@dataclass(frozen=True, kw_only=True)
class SendPaymentNotification(RpcCommand):
    """
    Send a payment notification.

    :param recipient: Specify the recipient's phone number.
    :param receipt: The base64 encoded receipt blob.
    :param note: Specify a note for the payment notification.
    """

    recipient: Optional[str] = None
    "Specify the recipient's phone number."
    receipt: str
    "The base64 encoded receipt blob."
    note: Optional[str] = None
    "Specify a note for the payment notification."


@dataclass(frozen=True, kw_only=True)
class SendReaction(RpcCommand):
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
    """

    emoji: str
    "Specify the emoji, should be a single unicode grapheme cluster."
    target_author: str
    "Specify the number of the author of the message to which to react."
    target_timestamp: int
    "Specify the timestamp of the message to which to react."
    group_ids: tuple[str, ...] = ()
    "Specify the recipient group ID."
    recipients: tuple[str, ...] = ()
    "Specify the recipients' phone number."
    usernames: tuple[str, ...] = ()
    "Specify the recipient username or username link."
    note_to_self: bool = False
    "Send the reaction to self without notification."
    remove: bool = False
    "Remove a reaction."
    story: bool = False
    "React to a story instead of a normal message"


@dataclass(frozen=True, kw_only=True)
class SendReceipt(RpcCommand):
    """
    Send a read or viewed receipt to a previously received message.

    :param recipient: Specify the sender's phone number.
    :param target_timestamps: Specify the timestamp of the messages for which a
        receipt should be sent.
    :param type: Specify the receipt type (default is read receipt).
    """

    recipient: str
    "Specify the sender's phone number."
    target_timestamps: NonEmptyTuple[int]
    "Specify the timestamp of the messages for which a receipt should be sent."
    type: Optional[Literal["read", "viewed"]] = None
    "Specify the receipt type (default is read receipt)."


@dataclass(frozen=True, kw_only=True)
class SendSyncRequest(RpcCommand):
    "Send a synchronization request message to primary device (for group, contacts, ...)."


@dataclass(frozen=True, kw_only=True)
class SendTyping(RpcCommand):
    """
    Send typing message to trigger a typing indicator for the recipient. Indicator
    will be shown for 15seconds unless a typing STOP message is sent first.

    :param group_ids: Specify the recipient group ID.
    :param recipients: Specify the recipients' phone number.
    :param stop: Send a typing STOP message.
    """

    group_ids: tuple[str, ...] = ()
    "Specify the recipient group ID."
    recipients: tuple[str, ...] = ()
    "Specify the recipients' phone number."
    stop: bool = False
    "Send a typing STOP message."


@dataclass(frozen=True, kw_only=True)
class SetPin(RpcCommand):
    """
    Set a registration lock pin, to prevent others from registering this number.

    :param pin: The registration lock PIN, that will be required for new
        registrations (resets after 7 days of inactivity)
    """

    pin: Optional[str] = None
    """
    The registration lock PIN, that will be required for new registrations (resets
    after 7 days of inactivity)
    """


@dataclass(frozen=True, kw_only=True)
class StartChangeNumber(RpcCommand):
    """
    Change account to a new phone number with SMS or voice verification.

    :param number: The new phone number in E164 format.
    :param captcha: The captcha token, required if change number failed with a
        captcha required error.
    :param voice: The verification should be done over voice, not SMS.
    """

    number: str
    "The new phone number in E164 format."
    captcha: Optional[str] = None
    "The captcha token, required if change number failed with a captcha required error."
    voice: bool = False
    "The verification should be done over voice, not SMS."


@dataclass(frozen=True, kw_only=True)
class SubmitRateLimitChallenge(RpcCommand):
    """
    Submit a captcha challenge to lift the rate limit. This command should only be
    necessary when sending fails with a proof required error.

    :param challenge: The challenge token taken from the proof required error.
    :param captcha: The captcha token from the solved captcha on the signal website.
    """

    challenge: str
    "The challenge token taken from the proof required error."
    captcha: str
    "The captcha token from the solved captcha on the signal website."


@dataclass(frozen=True, kw_only=True)
class Trust(RpcCommand):
    """
    Set the trust level of a given number.

    :param recipient: Specify the phone number, for which to set the trust.
    :param verified_safety_number: Specify the safety number of the key, only use
        this option if you have verified the safety number.
    :param trust_all_known_keys: Trust all known keys of this user, only use this for testing.
    """

    recipient: str
    "Specify the phone number, for which to set the trust."
    verified_safety_number: Optional[str] = None
    "Specify the safety number of the key, only use this option if you have verified the safety number."
    trust_all_known_keys: bool = False
    "Trust all known keys of this user, only use this for testing."

    @overload
    def __init__(self, *, recipient: str): ...

    @overload
    def __init__(self, *, recipient: str, verified_safety_number: str): ...

    @overload
    def __init__(self, *, recipient: str, trust_all_known_keys: Literal[True]): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := {"verified_safety_number", "trust_all_known_keys"})):
            case 0:
                raise ValueError(f"One of {args} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class Unblock(RpcCommand):
    """
    Unblock the given contacts or groups (messages will be received again)

    :param recipients: Contact number
    :param group_ids: Group ID
    """

    recipients: tuple[str, ...] = ()
    "Contact number"
    group_ids: tuple[str, ...] = ()
    "Group ID"


@dataclass(frozen=True, kw_only=True)
class Unregister(RpcCommand):
    """
    Unregister the current device from the signal server.

    :param delete_account: Delete account completely from server. CAUTION: Only do
        this if you won't use this number again!
    """

    delete_account: bool = False
    "Delete account completely from server. CAUTION: Only do this if you won't use this number again!"


@dataclass(frozen=True, kw_only=True)
class UpdateAccount(RpcCommand):
    """
    Update the account attributes on the signal server.

    :param device_name: Specify a name to describe this device.
    :param unrestricted_unidentified_sender: Enable if anyone should be able to send
        you unidentified sender messages.
    :param discoverable_by_number: Enable/disable if the account should be
        discoverable by phone number
    :param number_sharing: Indicates if Signal should share its phone number when sending a message.
    :param username: Specify a username that can then be used to contact this account.
    :param delete_username: Delete the username associated with this account.
    """

    device_name: Optional[str] = None
    "Specify a name to describe this device."
    unrestricted_unidentified_sender: Optional[bool] = None
    "Enable if anyone should be able to send you unidentified sender messages."
    discoverable_by_number: Optional[bool] = None
    "Enable/disable if the account should be discoverable by phone number"
    number_sharing: Optional[bool] = None
    "Indicates if Signal should share its phone number when sending a message."
    username: Optional[str] = None
    "Specify a username that can then be used to contact this account."
    delete_username: bool = False
    "Delete the username associated with this account."

    @overload
    def __init__(
        self,
        *,
        device_name: Optional[str] = None,
        unrestricted_unidentified_sender: Optional[bool] = None,
        discoverable_by_number: Optional[bool] = None,
        number_sharing: Optional[bool] = None,
    ): ...

    @overload
    def __init__(
        self,
        *,
        device_name: Optional[str] = None,
        unrestricted_unidentified_sender: Optional[bool] = None,
        discoverable_by_number: Optional[bool] = None,
        number_sharing: Optional[bool] = None,
        username: str,
    ): ...

    @overload
    def __init__(
        self,
        *,
        device_name: Optional[str] = None,
        unrestricted_unidentified_sender: Optional[bool] = None,
        discoverable_by_number: Optional[bool] = None,
        number_sharing: Optional[bool] = None,
        delete_username: Literal[True],
    ): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := {"username", "delete_username"})):
            case 0:
                raise ValueError(f"One of {args} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class UpdateConfiguration(RpcCommand):
    """
    Update signal configs and sync them to linked devices.

    :param read_receipts: Indicates if Signal should send read receipts.
    :param unidentified_delivery_indicators: Indicates if Signal should show
        unidentified delivery indicators.
    :param typing_indicators: Indicates if Signal should send/show typing indicators.
    :param link_previews: Indicates if Signal should generate link previews.
    """

    read_receipts: Optional[bool] = None
    "Indicates if Signal should send read receipts."
    unidentified_delivery_indicators: Optional[bool] = None
    "Indicates if Signal should show unidentified delivery indicators."
    typing_indicators: Optional[bool] = None
    "Indicates if Signal should send/show typing indicators."
    link_previews: Optional[bool] = None
    "Indicates if Signal should generate link previews."


@dataclass(frozen=True, kw_only=True)
class UpdateContact(RpcCommand):
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
    """

    recipient: Optional[str] = None
    "Contact number"
    name: Optional[str] = None
    "New contact name"
    given_name: Optional[str] = None
    "New system given name"
    family_name: Optional[str] = None
    "New system family name"
    nick_given_name: Optional[str] = None
    "New nick given name"
    nick_family_name: Optional[str] = None
    "New nick family name"
    note: Optional[str] = None
    "New note"
    expiration: Optional[int] = None
    "Set expiration time of messages (seconds)"


@dataclass(frozen=True, kw_only=True)
class UpdateGroup(RpcCommand):
    """
    Create or update a group.

    :param group_id: Specify the group ID.
    :param name: Specify the new group name.
    :param description: Specify the new group description.
    :param avatar: Specify a new group avatar image file
    :param link: Set group link state, with or without admin approval
    :param set_permission_add_member: Set permission to add new group members
    :param set_permission_edit_details: Set permission to edit group details
    :param set_permission_send_messages: Set permission to send messages
    :param expiration: Set expiration time of messages (seconds)
    :param members: Specify one or more members to add to the group
    :param remove_members: Specify one or more members to remove from the group
    :param admins: Specify one or more members to make a group admin
    :param remove_admins: Specify one or more members to remove group admin privileges
    :param bans: Specify one or more members to ban from joining the group
    :param unbans: Specify one or more members to remove from the ban list
    :param reset_link: Reset group link and create new link password
    """

    group_id: Optional[str] = None
    "Specify the group ID."
    name: Optional[str] = None
    "Specify the new group name."
    description: Optional[str] = None
    "Specify the new group description."
    avatar: Optional[str] = None
    "Specify a new group avatar image file"
    link: Optional[Literal["enabled", "enabled-with-approval", "disabled"]] = None
    "Set group link state, with or without admin approval"
    set_permission_add_member: Optional[Literal["every-member", "only-admins"]] = None
    "Set permission to add new group members"
    set_permission_edit_details: Optional[Literal["every-member", "only-admins"]] = None
    "Set permission to edit group details"
    set_permission_send_messages: Optional[Literal["every-member", "only-admins"]] = None
    "Set permission to send messages"
    expiration: Optional[int] = None
    "Set expiration time of messages (seconds)"
    members: tuple[str, ...] = ()
    "Specify one or more members to add to the group"
    remove_members: tuple[str, ...] = ()
    "Specify one or more members to remove from the group"
    admins: tuple[str, ...] = ()
    "Specify one or more members to make a group admin"
    remove_admins: tuple[str, ...] = ()
    "Specify one or more members to remove group admin privileges"
    bans: tuple[str, ...] = ()
    "Specify one or more members to ban from joining the group"
    unbans: tuple[str, ...] = ()
    "Specify one or more members to remove from the ban list"
    reset_link: bool = False
    "Reset group link and create new link password"


@dataclass(frozen=True, kw_only=True)
class UpdateProfile(RpcCommand):
    """
    Set a name, about and avatar image for the user profile

    :param given_name: New profile (given) name
    :param family_name: New profile family name (optional)
    :param about: New profile about text
    :param about_emoji: New profile about emoji
    :param mobile_coin_address: New MobileCoin address (Base64 encoded public address)
    :param avatar: Path to new profile avatar
    :param remove_avatar: None
    """

    given_name: Optional[str] = None
    "New profile (given) name"
    family_name: Optional[str] = None
    "New profile family name (optional)"
    about: Optional[str] = None
    "New profile about text"
    about_emoji: Optional[str] = None
    "New profile about emoji"
    mobile_coin_address: Optional[str] = None
    "New MobileCoin address (Base64 encoded public address)"
    avatar: Optional[str] = None
    "Path to new profile avatar"
    remove_avatar: bool = False

    @overload
    def __init__(
        self,
        *,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        about: Optional[str] = None,
        about_emoji: Optional[str] = None,
        mobile_coin_address: Optional[str] = None,
    ): ...

    @overload
    def __init__(
        self,
        *,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        about: Optional[str] = None,
        about_emoji: Optional[str] = None,
        mobile_coin_address: Optional[str] = None,
        avatar: str,
    ): ...

    @overload
    def __init__(
        self,
        *,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        about: Optional[str] = None,
        about_emoji: Optional[str] = None,
        mobile_coin_address: Optional[str] = None,
        remove_avatar: Literal[True],
    ): ...

    def __init__(self, **kwargs):
        self.__dict__.update({f.name: f.default for f in fields(self) if f.default != MISSING})
        self.__dict__.update(kwargs)
        match len(kwargs.keys() & (args := {"avatar", "remove_avatar"})):
            case 0:
                raise ValueError(f"One of {args} is required!")
            case 1:
                pass
            case _:
                raise ValueError(f"Arguments {args} are mutually exclusive!")


@dataclass(frozen=True, kw_only=True)
class UploadStickerPack(RpcCommand):
    """
    Upload a new sticker pack, consisting of a manifest file and the stickers images.

    :param path: The path of the manifest.json or a zip file containing the sticker
        pack you wish to upload.
    """

    path: Optional[str] = None
    "The path of the manifest.json or a zip file containing the sticker pack you wish to upload."


@dataclass(frozen=True, kw_only=True)
class Version(RpcCommand):
    pass
