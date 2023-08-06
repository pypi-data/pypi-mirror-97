Convenience functions and classes to work with email.
      - Cameron Simpson <cs@cskk.id.au>
#

*Latest release 20210306*:
New RFC5322_DATE_TIME with format for datetime.strptime to emit an RFC5322 date-time token.

## Function `ismaildir(path)`

Test if `path` points at a Maildir directory.

## Function `ismbox(path)`

Open path and check that its first line begins with "From ".

## Function `ismhdir(path)`

Test if `path` points at an MH directory.

## Class `Maildir(mailbox.Maildir,mailbox.Mailbox)`

A faster Maildir interface.
Trust os.listdir, don't fsync, etc.

### Method `Maildir.__getitem__(self, key)`

Return a mailbox.Message loaded from the message with key `key`.
The Message's .pathname property contains .keypath(key),
the pathname to the message file.

### Method `Maildir.add(self, message, key=None)`

Add a message to the Maildir.
`message` may be an email.message.Message instance or a path to a file.

### Method `Maildir.as_mbox(self, fp, keys=None)`

Transcribe the contents of this maildir in UNIX mbox format to the
file `fp`.
The optional iterable `keys` designates the messages to transcribe.
The default is to transcribe all messages.

### Method `Maildir.flush(self)`

Forget state.

### Method `Maildir.get_headers(self, key)`

Return the headers of the specified message as

### Method `Maildir.get_message(self, key)`

Return a mailbox.Message loaded from the message with key `key`.
The Message's .pathname property contains .keypath(key),
the pathname to the message file.

### Method `Maildir.iterheaders(self)`

Yield (key, headers) from the Maildir.

### Method `Maildir.keypath(self, key)`

Return the path to the message with maildir key `key`.

### Property `Maildir.msgmap`

Scan the maildir, return key->message-info mapping.

### Method `Maildir.newkey(self)`

Allocate a new key.

### Method `Maildir.open(self, key, mode='r')`

Open the file storing the message specified by `key`.

### Method `Maildir.save_file(self, fp, key=None, flags='')`

Save the contents of the file-like object `fp` into the Maildir.
Return the key for the saved message.

### Method `Maildir.save_filepath(self, filepath, key=None, nolink=False, flags='')`

Save the file specified by `filepath` into the Maildir.
By default a hardlink is attempted unless `nolink` is supplied true.
The optional `flags` is a string consisting of flag letters listed at:
  http://cr.yp.to/proto/maildir.html
Return the key for the saved message.

### Method `Maildir.save_message(self, M, key=None, flags='')`

Save the contents of the Message `M` into the Maildir.
Return the key for the saved message.

## Function `make_maildir(path)`

Create a new maildir at `path`.
The path must not already exist.

## Function `Message(msgfile, headersonly=False)`

Factory function to accept a file or filename and return an email.message.Message.

## Function `message_addresses(M, header_names)`

Yield (realname, address) pairs from all the named headers.

## Function `modify_header(M, hdr, new_values, always=False)`

Modify a Message `M` to change the value of the named header `hdr` to the new value `new_values` (a string or an interable of strings).
If `new_values` is a string subclass, convert to a single element list.
If `new_values` differs from the existing value or if `always`
is true, save the old value as X-Old-`hdr`.
Return a Boolean indicating whether the headers were modified.

# Release Log



*Release 20210306*:
New RFC5322_DATE_TIME with format for datetime.strptime to emit an RFC5322 date-time token.

*Release 20171231.1*:
DISTINFO fix. No semantic changes.

*Release 20171231*:
Update imports, clean some lint. No semantic changes.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* modify_header: accept multiple header values.
* Message factory function: open message files with errors="replace" because messages might have any arbitrary guff in them; accept the mangling that may occur.
* Add new_message_id() and need_message_id().
* Add message_references() to return related Message-IDs from Reply-To: and References: headers.
* Python 2/3 portability fixes.
* Assorted bugfixes and improvements.

*Release 20150116.2*:
Update PyPI metadata.

*Release 20150116*:
Initial PyPI release.
