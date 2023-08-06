1.4.0
~~~~~~~~~~~~

#77 Fixed yet another demandimport problem (cryptography.utils
failure on Fedora with Python3.8).

Fixed various py3 incompatibilities (thanks to Matt Harbison).

1.3.2
~~~~~~~~~~~~

Added keyring backends to demandimport ignores. This resolves
problems with running the extension in some environments / with
some keyring versions (reported problems include keyring 22.0.1
on MacOS, and Python 3.9 in general).

1.3.1
~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket.

1.3.0
~~~~~~~~~~~~

#33 Python3-based Mercurial installs are supported and should work -
including sharing passwords with Python2 installations.

Note: remember about installing proper keyring backend dependencies
under py3 (like python-dbus). Those aren't shared!


1.2.1
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

1.2.0
~~~~~~~~~~~~

#62 Compatible with Mercurial 4.7 (some fixes were needed to avoid
crashes while working in this version). Most important fixes were made
in meu (so here we just depend on proper version), but there are also
individual fixes here (related to smtp handling).

#61 In case keyring library raises exceptions (like recent versions do
when no backend is available), we don't crash mercurial anymore.
mercurial_keyring emits the warning and falls back to normal password
handling (propts).

Refreshing smtp monkeypatch to be a bit more like modern mercurials
(in particular, obligatory cert falidaton).

1.1.9
~~~~~~~~~~~~

4.6-compatibility, 4.5-testing.

1.1.8
~~~~~~~~~~~~~

Updated links after bitbucket changes.

1.1.7
~~~~~~~~~~~~~~~~~~

#52 hg keyring_check and hg keyring_clear did not work since
Mercurial 3.9 (incompatibility caused by commit 2c019aac6b99,
introducing passwdb).

1.1.6
~~~~~~~~~~~~~~~~~~

Fixed NameError showing up in some password saving scenarios, in
particular in case of password save failures (thanks to Andrew
Taumoefolau for reporting and fixing).

1.1.5
~~~~~~~~~~~~~~~~~~

Mercurial 3.9 compatibility.

1.1.4
~~~~~~~~~~~~~~~~~~

Gracefully handle failures to save passwords - they are reported
as warnings, but don't break the operation being executed.

Compatibility fixes for upcoming 3.9 release (which changes SSL API
noticeably, what impact SMTP passwords handling in mercurial_keyring).

1.1.3
~~~~~~~~~~~~~~~~~~

Mercurial 3.8 compatibility for email over SSL/TLS (SMTPS/STARTTLS
constructors changed). Should not spoil older versions.

1.1.2
~~~~~~~~~~~~~~~~~~

The keyring_check and keyring_clear commands can be run outside
repository (if given some path as parameter).

Fixed some messages.

README updates (a few language fixes, added note about GUI tools).

1.1.1
~~~~~~~~~~~~~~~~~~

#49 Fixed the bug due to url-stored usernames did not work (introduced
in 1.0.0 and not completely fixed in 1.0.1).

#50 Bad doc url in error message


1.1.0
~~~~~~~~~~~~~~~~~~

Forward compatibility for Mercurial 3.8 (should not break old mercurials)

1.0.1
~~~~~~~~~~~~~~~~~~

URLs containing usernames (https://John@some.service/somewhat) were
not working unless username was also configured separately (username
presence in url was not detected properly).

Liberated prefix matching, path https://John@some.service/somewhat can
be matched both against prefix https://some.service and against
https://John@some.service. That mostly matches what mercurial itself
does.

1.0.0
~~~~~~~~~~~~~~~~~~

Added
    hg keyring_check
and
    hg keyring_clear PATH-OR-ALIAS
commands

Removed obsolete workarounds (compatibility for very old Mercurials -
some for pre-1.0, some for 1.4, some for 1.8/1.9). 
Mercurial 2.0 is now required.

Improved information about path prefix. In particular it is shown
whenever user is asked for password, for example:
     hg pull bitbucket
     http authorization required
     realm: BitBucket
     url: https://bitbucket.org/Mekk
     user: Mekk (fixed in hgrc or url)
     password: 

Improved README.

Improved debug information.

0.8.0
~~~~~~~~~~~~~~~~~~

Module is simplified a bit, but requires mercurial_extension_utils.
Debug messages are prefixed with keyring: not [HgKeyring]

0.7.1
~~~~~~~~~~~~~~~~~~

#48 NullHandler import failure no longer breaks the extension.
May help python 2.6 compatibility.

0.7.0
~~~~~~~~~~~~~~~~~~~

Delaying keyring module import until passwords are really needed. It
can noticeably improve Mercurial (non pull/push) performance in some
cases (no longer slow hg status because D-Bus is busy an keyring tries
to activate KDE Wallet through it…).

0.6.7
~~~~~~~~~~~~~~~~~

#46 Fixed syntax of smtp.tls configuration setting (current Mercurials
doesn't handle "true" anymore, TortoiseHG crashed with mercurial
keyring enabled while currently recommended starttls/smtps/none values
were in use).

0.6.6
~~~~~~~~~~~~~~~~~ 

#44 Handling some more mercurial versions in demandimport-detection
logic.

0.6.5
~~~~~~~~~~~~~~~~~

#36 Shutting up warning about no logging handlers.

0.6.4
~~~~~~~~~~~~~~~~~

#44 Pre-2.9.1 Mercurials compatibility (probing for active
demandimport differently).

0.6.3
~~~~~~~~~~~~~~~~~

#41 Fix for incorrect demandimport activity check logic, which could
cause various problems with imports after mercurial_keyring is
imported.

0.6.2
~~~~~~~~~~~~~~~~~

#33 Fix for UnicodeDecodeErrors happening on some backends (especially
Vault) when passwords with non-ascii characters are in use and native
locale is not utf-8. Passwords are no longer saved to keyring backends
as-entered, they are now decoded from local encoding (whichever is
detected by Mercurial), then encoded to unicode.

0.6.1
~~~~~~~~~~~~~~~~~

#30 Yet another demandimport conflict fixed.

0.6.0
~~~~~~~~~~~~~~~~~

#28 Disable demandimport completely during keyring import. Mayhaps it
will resolve (most) demandimport conflict errors.

0.5.7
~~~~~~~~~~~~~~~~~

#27 Some more demandimport ignores.

0.5.6
~~~~~~~~~~~~~~~~~

#24, #25 Demandimport fixes (import failures in specific cases).

Better way of demandimport-ignoring modules. In particular, we append
more of them if gobject happens to be on the list.

0.5.5
~~~~~~~~~~~~~~~~~

Fix for gnome keyring import problems.

0.5.4
~~~~~~~~~~~~~~~~~

#22 Some more demandimport ignores (fix import failures).

SMTP password was not cleared properly (after detecting that it is
invalid).

Clarified license to be modified BSD style license.

0.5.3
~~~~~~~~~~~~~~~~~

Remove useless import which caused problems on Mercurial 2.3 when
demandimport was not enabled

0.5.1
~~~~~~~~~~~~~~~~~

Add help text to output for hg help.

0.5.0
~~~~~~~~~~~~~~~~~

Improved bad password detection. Internally: extension is now able to
properly differentiate between an authentication failure and a new
request to the same url.

Fixes in debug message

Further debug messages patching

Improving debug messages handling.

Mercurial Keyring debug messages are now prefixed with
[HgKeyring] to make distinguishing them easier

0.4.6
~~~~~~~~~~~~~~~~~

More compatibility (changed signature of httpconnection.readauthforuri
, introduced post Mercurial 1.9 - since hg.0593e8f81c71)

Fix compatibility code which did not work due to demandimport issues
(attempts to catch ImportErrors on "from mercurial.url import
readauthforuri" were not working properly).

0.4.5
~~~~~~~~~~~~~~~~~

Mercurial 1.9 compatibility (readauthforuri has been moved into new
httpconnection module).

0.4.4
~~~~~~~~~~~~~~~~~

Mercurial 1.8 compatibility (passwordmgr.readauthtoken() has been
moved into mercurial.url.readauthforuri).

0.4.3
~~~~~~~~~~~~~~~~~

Keyring fork no longer is needed as keyring releases are available
again.

Workaround for gnomekeyring mercurial.demandimport incompatibility:
mercurial.demandimport, which is enabled while in a mercurial
extensions, prevents the correct import of gobject._gobject and
consequently doesn't allow the loading of the gnomekeyring module,
which can be used by keyring. This just adds the proper module to
demandimport ignore list.

0.4.2
~~~~~~~~~~~~~~~~~

No longer raising an error when username is specified both in ~/.hgrc
and <repo>/.hg/hgrc if it is the same in both places.

Docs recommend sborho keyring fork.

0.4.1
~~~~~~~~~~~~~~~~~

Some tweaks and docs related to prefix handling.

Explicit information that keyring is not used due to lack of username.

0.4.0
~~~~~~~~~~~~~~~~~

Store and lookup prefix from [auth] so that password is shared amongst
shared auth entries

0.3.3
~~~~~~~~~~~~~~~~~

Better error message

0.3.2
~~~~~~~~~~~~~~~~~

Doc tweaks

0.3.1
~~~~~~~~~~~~~~~~~

Introduced and documented PyPi package, added setup.py

0.2.0
~~~~~~~~~~~~~~~~~

Added handling of SMTP passwords (tested on patchbomb extension but
should work on anything what utilizes mercurial.mail)

Docstrings mention Debian keyring packages.

0.1.1
~~~~~~~~~~~~~~~~~

Initial public release
