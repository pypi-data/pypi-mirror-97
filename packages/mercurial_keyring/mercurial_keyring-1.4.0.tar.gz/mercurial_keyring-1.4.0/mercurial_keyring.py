# -*- coding: utf-8 -*-
#
# mercurial_keyring: save passwords in password database
#
# Copyright (c) 2009 Marcin Kasperski <Marcin.Kasperski@mekk.waw.pl>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# See README.rst for more details.

'''securely save HTTP and SMTP passwords to encrypted storage

mercurial_keyring securely saves HTTP and SMTP passwords in password
databases (Gnome Keyring, KDE KWallet, OSXKeyChain, Win32 crypto
services).

The process is automatic.  Whenever bare Mercurial just prompts for
the password, Mercurial with mercurial_keyring enabled checks whether
saved password is available first.  If so, it is used.  If not, you
will be prompted for the password, but entered password will be
saved for the future use.

In case saved password turns out to be invalid (HTTP or SMTP login
fails) it is dropped, and you are asked for current password.

Actual password storage is implemented by Python keyring library, this
extension glues those services to Mercurial. Consult keyring
documentation for information how to configure actual password
backend (by default keyring guesses, usually correctly, for example
you get KDE Wallet under KDE, and Gnome Keyring under Gnome or Unity).
'''

import socket
import os
import sys
import re
if sys.version_info[0] < 3:
    from urllib2 import (
        HTTPPasswordMgrWithDefaultRealm, AbstractBasicAuthHandler, AbstractDigestAuthHandler)
else:
    from urllib.request import (
        HTTPPasswordMgrWithDefaultRealm, AbstractBasicAuthHandler, AbstractDigestAuthHandler)
import smtplib

from mercurial import util, sslutil, error
from mercurial.i18n import _
from mercurial.url import passwordmgr
from mercurial import mail
from mercurial.mail import SMTPS, STARTTLS
from mercurial import encoding
from mercurial import ui as uimod

# pylint: disable=invalid-name, line-too-long, protected-access, too-many-arguments

###########################################################################
# Specific import trickery
###########################################################################


def import_meu():
    """
    Convoluted import of mercurial_extension_utils, which helps
    TortoiseHg/Win setups. This routine and it's use below
    performs equivalent of
        from mercurial_extension_utils import monkeypatch_method
    but looks for some non-path directories.
    """
    try:
        import mercurial_extension_utils
    except ImportError:
        my_dir = os.path.dirname(__file__)
        sys.path.extend([
            # In the same dir (manual or site-packages after pip)
            my_dir,
            # Developer clone
            os.path.join(os.path.dirname(my_dir), "extension_utils"),
            # Side clone
            os.path.join(os.path.dirname(my_dir), "mercurial-extension_utils"),
        ])
        try:
            import mercurial_extension_utils
        except ImportError:
            raise error.Abort(_(b"""Can not import mercurial_extension_utils.
Please install this module in Python path.
See Installation chapter in https://foss.heptapod.net/mercurial/mercurial_keyring/ for details
(and for info about TortoiseHG on Windows, or other bundled Python)."""))
    return mercurial_extension_utils


meu = import_meu()
monkeypatch_method = meu.monkeypatch_method


def import_keyring():
    """
    Importing keyring happens to be costly if wallet is slow, so we delay it
    until it is really needed. The routine below also works around various
    demandimport-related problems.
    """
    # mercurial.demandimport incompatibility workaround.
    # various keyring backends fail as they can't properly import helper
    # modules (as demandimport modifies python import behaviour).
    # If you get import errors with demandimport in backtrace, try
    # guessing what to block and extending the list below.
    mod, was_imported_now = meu.direct_import_ext(
        "keyring", [
            "gobject._gobject",
            "configparser",
            "json",
            "abc",
            "io",
            "keyring",
            "keyring.backends.SecretService",
            "keyring.backends.Windows",
            "keyring.backends.chainer",
            "keyring.backends.fail",
            "keyring.backends.kwallet",
            "keyring.backends.macOS",
            "gdata.docs.service",
            "gdata.service",
            "types",
            "atom.http",
            "atom.http_interface",
            "atom.service",
            "atom.token_store",
            "ctypes",
            "secretstorage.exceptions",
            "fs.opener",
            "win32ctypes.pywin32",
            "win32ctypes.pywin32.pywintypes",
            "win32ctypes.pywin32.win32cred",
            "pywintypes",
            "win32cred",
            "cryptography.utils",
        ])
    if was_imported_now:
        # Shut up warning about uninitialized logging by keyring
        meu.disable_logging("keyring")
    return mod


#################################################################
# Actual implementation
#################################################################

KEYRING_SERVICE = "Mercurial"


class PasswordStore(object):
    """
    Helper object handling keyring usage (password save&restore,
    the way passwords are keyed in the keyring).
    """
    def __init__(self):
        self.cache = dict()

    def get_http_password(self, url, username):
        """
        Checks whether password of username for url is available,
        returns it or None
        """
        return self._read_password_from_keyring(
            self._format_http_key(url, username))

    def set_http_password(self, url, username, password):
        """Saves password to keyring"""
        self._save_password_to_keyring(
            self._format_http_key(url, username),
            password)

    def clear_http_password(self, url, username):
        """Drops saved password"""
        self.set_http_password(url, username, b"")

    @staticmethod
    def _format_http_key(url, username):
        """Construct actual key for password identification"""
        # keyring expects str, mercurial feeds as here mostly with bytes
        key = "%s@@%s" % (meu.pycompat.sysstr(username),
                          meu.pycompat.sysstr(url))
        return key

    @staticmethod
    def _format_smtp_key(machine, port, username):
        """Construct key for SMTP password identification"""
        key = "%s@@%s:%s" % (meu.pycompat.sysstr(username),
                             meu.pycompat.sysstr(machine),
                             str(port))
        return key

    def get_smtp_password(self, machine, port, username):
        """Checks for SMTP password in keyring, returns
        password or None"""
        return self._read_password_from_keyring(
            self._format_smtp_key(machine, port, username))

    def set_smtp_password(self, machine, port, username, password):
        """Saves SMTP password to keyring"""
        self._save_password_to_keyring(
            self._format_smtp_key(machine, port, username),
            password)

    def clear_smtp_password(self, machine, port, username):
        """Drops saved SMTP password"""
        self.set_smtp_password(machine, port, username, "")

    @staticmethod
    def _read_password_from_keyring(pwdkey):
        """Physically read from keyring"""
        keyring = import_keyring()
        try:
            password = keyring.get_password(KEYRING_SERVICE, pwdkey)
        except Exception as err:
            ui = uimod.ui()
            ui.warn(meu.ui_string(
                b"keyring: keyring backend doesn't seem to work, password can not be restored. Falling back to prompts. Error details: %s\n",
                err))
            return b''
        # Reverse recoding from next routine
        if isinstance(password, meu.pycompat.unicode):
            return encoding.tolocal(password.encode('utf-8'))
        return password

    @staticmethod
    def _save_password_to_keyring(pwdkey, password):
        """Physically write to keyring"""
        keyring = import_keyring()
        # keyring in general expects unicode.
        # Mercurial provides "local" encoding. See #33.
        # py3 adds even more fun as we get already unicode from getpass.
        # To handle those quirks, let go through encoding.fromlocal in case we
        # got bytestr here, this will handle both normal py2 and emergency py3 cases.
        if isinstance(password, bytes):
            password = encoding.fromlocal(password).decode('utf-8')
        try:
            keyring.set_password(
                KEYRING_SERVICE, pwdkey, password)
        except Exception as err:
            ui = uimod.ui()
            ui.warn(meu.ui_string(
                b"keyring: keyring backend doesn't seem to work, password was not saved. Error details: %s\n",
                err))


password_store = PasswordStore()


############################################################
# Various utils
############################################################

class PwdCache(object):
    """Short term cache, used to preserve passwords
    if they are used twice during a command"""
    def __init__(self):
        self._cache = {}

    def store(self, realm, url, user, pwd):
        """Saves password"""
        cache_key = (realm, url, user)
        self._cache[cache_key] = pwd

    def check(self, realm, url, user):
        """Checks for cached password"""
        cache_key = (realm, url, user)
        return self._cache.get(cache_key)


_re_http_url = re.compile(b'^https?://')


def is_http_path(url):
    return bool(_re_http_url.search(url))


def make_passwordmgr(ui):
    """Constructing passwordmgr in a way compatible with various mercurials"""
    if hasattr(ui, 'httppasswordmgrdb'):
        return passwordmgr(ui, ui.httppasswordmgrdb)
    else:
        return passwordmgr(ui)  # pytype: disable=missing-parameter

############################################################
# HTTP password management
############################################################


class HTTPPasswordHandler(object):
    """
    Actual implementation of password handling (user prompting,
    configuration file searching, keyring save&restore).

    Object of this class is bound as passwordmgr attribute.
    """
    def __init__(self):
        self.pwd_cache = PwdCache()
        self.last_reply = None

    # Markers and also names used in debug notes. Password source
    SRC_URL = "repository URL"
    SRC_CFGAUTH = "hgrc"
    SRC_MEMCACHE = "temporary cache"
    SRC_URLCACHE = "urllib temporary cache"
    SRC_KEYRING = "keyring"

    def get_credentials(self, pwmgr, realm, authuri, skip_caches=False):
        """
        Looks up for user credentials in various places, returns them
        and information about their source.

        Used internally inside find_auth and inside informative
        commands (thiis method doesn't cache, doesn't detect bad
        passwords etc, doesn't prompt interactively, doesn't store
        password in keyring).

        Returns: user, password, SRC_*, actual_url

        If not found, password and SRC is None, user can be given or
        not, url is always set
        """
        ui = pwmgr.ui

        parsed_url, url_user, url_passwd = self.unpack_url(authuri)
        base_url = bytes(parsed_url)
        ui.debug(meu.ui_string(b'keyring: base url: %s, url user: %s, url pwd: %s\n',
                               base_url, url_user, url_passwd and b'******' or b''))

        # Extract username (or password) stored directly in url
        if url_user and url_passwd:
            return url_user, url_passwd, self.SRC_URL, base_url

        # Extract data from urllib (in case it was already stored)
        if isinstance(pwmgr, HTTPPasswordMgrWithDefaultRealm):
            urllib_user, urllib_pwd = \
                HTTPPasswordMgrWithDefaultRealm.find_user_password(
                    pwmgr, realm, authuri)
        else:
            urllib_user, urllib_pwd = pwmgr.passwddb.find_user_password(
                realm, authuri)
        if urllib_user and urllib_pwd:
            return urllib_user, urllib_pwd, self.SRC_URLCACHE, base_url

        actual_user = url_user or urllib_user

        # Consult configuration to normalize url to prefix, and find username
        # (and maybe password)
        auth_user, auth_pwd, keyring_url = self.get_url_config(
            ui, parsed_url, actual_user)
        if auth_user and actual_user and (actual_user != auth_user):
            raise error.Abort(_(b'keyring: username for %s specified both in repository path (%s) and in .hg/hgrc/[auth] (%s). Please, leave only one of those' % (base_url, actual_user, auth_user)))
        if auth_user and auth_pwd:
            return auth_user, auth_pwd, self.SRC_CFGAUTH, keyring_url

        actual_user = actual_user or auth_user

        if skip_caches:
            return actual_user, None, None, keyring_url

        # Check memory cache (reuse )
        # Checking the memory cache (there may be many http calls per command)
        cached_pwd = self.pwd_cache.check(realm, keyring_url, actual_user)
        if cached_pwd:
            return actual_user, cached_pwd, self.SRC_MEMCACHE, keyring_url

        # Load from keyring.
        if actual_user:
            ui.debug(meu.ui_string(b"keyring: looking for password (user %s, url %s)\n",
                                   actual_user, keyring_url))
            keyring_pwd = password_store.get_http_password(keyring_url, actual_user)
            if keyring_pwd:
                return actual_user, keyring_pwd, self.SRC_KEYRING, keyring_url

        return actual_user, None, None, keyring_url

    @staticmethod
    def prompt_interactively(ui, user, realm, url):
        """Actual interactive prompt"""
        if not ui.interactive():
            raise error.Abort(_(b'keyring: http authorization required but program used in non-interactive mode'))

        if not user:
            ui.status(meu.ui_string(b"keyring: username not specified in hgrc (or in url). Password will not be saved.\n"))

        ui.write(meu.ui_string(b"http authorization required\n"))
        ui.status(meu.ui_string(b"realm: %s\n",
                                realm))
        ui.status(meu.ui_string(b"url: %s\n",
                                url))
        if user:
            ui.write(meu.ui_string(b"user: %s (fixed in hgrc or url)\n",
                                   user))
        else:
            user = ui.prompt(meu.ui_string(b"user:"),
                             default=None)
        pwd = ui.getpass(meu.ui_string(b"password: "))
        return user, pwd

    def find_auth(self, pwmgr, realm, authuri, req):
        """
        Actual implementation of find_user_password - different
        ways of obtaining the username and password.

        Returns pair username, password
        """
        ui = pwmgr.ui
        after_bad_auth = self._after_bad_auth(ui, realm, authuri, req)

        # Look in url, cache, etc
        user, pwd, src, final_url = self.get_credentials(
            pwmgr, realm, authuri, skip_caches=after_bad_auth)
        if pwd:
            if src != self.SRC_MEMCACHE:
                self.pwd_cache.store(realm, final_url, user, pwd)
            self._note_last_reply(realm, authuri, user, req)
            ui.debug(meu.ui_string(b"keyring: Password found in %s\n",
                                   src))
            return user, pwd

        # Last resort: interactive prompt
        user, pwd = self.prompt_interactively(ui, user, realm, final_url)

        if user:
            # Saving password to the keyring.
            # It is done only if username is permanently set.
            # Otherwise we won't be able to find the password so it
            # does not make much sense to preserve it
            ui.debug(meu.ui_string(b"keyring: Saving password for %s to keyring\n",
                                   user))
            try:
                password_store.set_http_password(final_url, user, pwd)
            except Exception as e:
                keyring = import_keyring()
                if isinstance(e, keyring.errors.PasswordSetError):
                    ui.traceback()
                    ui.warn(meu.ui_string(b"warning: failed to save password in keyring\n"))
                else:
                    raise e

        # Saving password to the memory cache
        self.pwd_cache.store(realm, final_url, user, pwd)
        self._note_last_reply(realm, authuri, user, req)
        ui.debug(meu.ui_string(b"keyring: Manually entered password\n"))
        return user, pwd

    def get_url_config(self, ui, parsed_url, user):
        """
        Checks configuration to decide whether/which username, prefix,
        and password are configured for given url. Consults [auth] section.

        Returns tuple (username, password, prefix) containing elements
        found. username and password can be None (if unset), if prefix
        is not found, url itself is returned.
        """
        from mercurial.httpconnection import readauthforuri
        ui.debug(meu.ui_string(b"keyring: checking for hgrc info about url %s, user %s\n",
                               parsed_url, user))

        res = readauthforuri(ui, bytes(parsed_url), user)
        # If it user-less version not work, let's try with added username to handle
        # both config conventions
        if (not res) and user:
            parsed_url.user = user
            res = readauthforuri(ui, bytes(parsed_url), user)
            parsed_url.user = None
        if res:
            group, auth_token = res
        else:
            auth_token = None

        if auth_token:
            username = auth_token.get(b'username')
            password = auth_token.get(b'password')
            prefix = auth_token.get(b'prefix')
        else:
            username = user
            password = None
            prefix = None

        password_url = self.password_url(bytes(parsed_url), prefix)

        ui.debug(meu.ui_string(b"keyring: Password url: %s, user: %s, password: %s (prefix: %s)\n",
                               password_url, username,
                               b'********' if password else b'',
                               prefix))

        return username, password, password_url

    def _note_last_reply(self, realm, authuri, user, req):
        """
        Internal helper. Saves info about auth-data obtained,
        preserves them in last_reply, and returns pair user, pwd
        """
        self.last_reply = dict(realm=realm, authuri=authuri,
                               user=user, req=req)

    def _after_bad_auth(self, ui, realm, authuri, req):
        """
        If we are called again just after identical previous
        request, then the previously returned auth must have been
        wrong. So we note this to force password prompt (and avoid
        reusing bad password indefinitely).

        This routine checks for this condition.
        """
        if self.last_reply:
            if (self.last_reply['realm'] == realm) \
               and (self.last_reply['authuri'] == authuri) \
               and (self.last_reply['req'] == req):
                ui.debug(meu.ui_string(
                    b"keyring: Working after bad authentication, cached passwords not used %s\n",
                    str(self.last_reply)))
                return True
        return False

    @staticmethod
    def password_url(base_url, prefix):
        """Calculates actual url identifying the password. Takes
        configured prefix under consideration (so can be shorter
        than repo url)"""
        if not prefix or prefix == b'*':
            return base_url
        scheme, hostpath = base_url.split(b'://', 1)
        p = prefix.split(b'://', 1)
        if len(p) > 1:
            prefix_host_path = p[1]
        else:
            prefix_host_path = prefix
        password_url = scheme + b'://' + prefix_host_path
        return password_url

    @staticmethod
    def unpack_url(authuri):
        """
        Takes original url for which authentication is attempted and:

        - Strips query params from url. Used to convert urls like
          https://repo.machine.com/repos/apps/module?pairs=0000000000000000000000000000000000000000-0000000000000000000000000000000000000000&cmd=between
          to
          https://repo.machine.com/repos/apps/module

        - Extracts username and password, if present, and removes them from url
          (so prefix matching works properly)

        Returns url, user, password
        where url is mercurial.util.url object already stripped of all those
        params.
        """
        # In case of py3, util.url expects bytes
        authuri = meu.pycompat.bytestr(authuri)

        # mercurial.util.url, rather handy url parser
        parsed_url = util.url(authuri)
        parsed_url.query = b''
        parsed_url.fragment = None
        # Strip arguments to get actual remote repository url.
        # base_url = "%s://%s%s" % (parsed_url.scheme, parsed_url.netloc,
        #                       parsed_url.path)
        user = parsed_url.user
        passwd = parsed_url.passwd
        parsed_url.user = None
        parsed_url.passwd = None

        return parsed_url, user, passwd


############################################################
# Mercurial monkey-patching
############################################################


@monkeypatch_method(passwordmgr)
def find_user_password(self, realm, authuri):
    """
    keyring-based implementation of username/password query
    for HTTP(S) connections

    Passwords are saved in gnome keyring, OSX/Chain or other platform
    specific storage and keyed by the repository url
    """
    # In sync with hg 5.0
    assert isinstance(realm, (type(None), str))
    assert isinstance(authuri, str)

    # Extend object attributes
    if not hasattr(self, '_pwd_handler'):
        self._pwd_handler = HTTPPasswordHandler()

    if hasattr(self, '_http_req'):
        req = self._http_req
    else:
        req = None

    return self._pwd_handler.find_auth(self, realm, authuri, req)


@monkeypatch_method(AbstractBasicAuthHandler, "http_error_auth_reqed")
def basic_http_error_auth_reqed(self, authreq, host, req, headers):
    """Preserves current HTTP request so it can be consulted
    in find_user_password above"""
    self.passwd._http_req = req
    try:
        return basic_http_error_auth_reqed.orig(self, authreq, host, req, headers)
    finally:
        self.passwd._http_req = None


@monkeypatch_method(AbstractDigestAuthHandler, "http_error_auth_reqed")
def digest_http_error_auth_reqed(self, authreq, host, req, headers):
    """Preserves current HTTP request so it can be consulted
    in find_user_password above"""
    self.passwd._http_req = req
    try:
        return digest_http_error_auth_reqed.orig(self, authreq, host, req, headers)
    finally:
        self.passwd._http_req = None

############################################################
# SMTP support
############################################################


def try_smtp_login(ui, smtp_obj, username, password):
    """
    Attempts smtp login on smtp_obj (smtplib.SMTP) using username and
    password.

    Returns:
    - True if login succeeded
    - False if login failed due to the wrong credentials

    Throws Abort exception if login failed for any other reason.

    Immediately returns False if password is empty
    """
    if not password:
        return False
    try:
        ui.note(_(b'(authenticating to mail server as %s)\n') %
                username)
        smtp_obj.login(username, password)
        return True
    except smtplib.SMTPException as inst:
        if inst.smtp_code == 535:
            ui.status(meu.ui_string(b"SMTP login failed: %s\n\n",
                                    inst.smtp_error))
            return False
        else:
            raise error.Abort(inst)


def keyring_supported_smtp(ui, username):
    """
    keyring-integrated replacement for mercurial.mail._smtp Used only
    when configuration file contains username, but does not contain
    the password.

    Most of the routine below is copied as-is from
    mercurial.mail._smtp.  The critical changed part is marked with #
    >>>>> and # <<<<< markers, there are also some fixes which make
    the code working on various Mercurials (like parsebool import).
    """
    try:
        from mercurial.utils.stringutil import parsebool
    except ImportError:
        from mercurial.utils import parsebool  # pytype: disable=import-error

    local_hostname = ui.config(b'smtp', b'local_hostname')
    tls = ui.config(b'smtp', b'tls', b'none')
    # backward compatible: when tls = true, we use starttls.
    starttls = tls == b'starttls' or parsebool(tls)
    smtps = tls == b'smtps'
    if (starttls or smtps) and not util.safehasattr(socket, 'ssl'):
        raise error.Abort(_(b"can't use TLS: Python SSL support not installed"))
    mailhost = ui.config(b'smtp', b'host')
    if not mailhost:
        raise error.Abort(_(b'smtp.host not configured - cannot send mail'))
    if getattr(sslutil, 'sslkwargs', None) is None:
        sslkwargs = None
    elif starttls or smtps:
        sslkwargs = sslutil.sslkwargs(ui, mailhost)  # pytype: disable=module-attr
    else:
        sslkwargs = {}
    if smtps:
        ui.note(_(b'(using smtps)\n'))

        # mercurial 3.8 added a mandatory host arg
        if not sslkwargs:
            s = SMTPS(ui, local_hostname=local_hostname, host=mailhost)
        elif 'host' in SMTPS.__init__.__code__.co_varnames:
            s = SMTPS(sslkwargs, local_hostname=local_hostname, host=mailhost)
        else:
            s = SMTPS(sslkwargs, local_hostname=local_hostname)
    elif starttls:
        if not sslkwargs:
            s = STARTTLS(ui, local_hostname=local_hostname, host=mailhost)
        elif 'host' in STARTTLS.__init__.__code__.co_varnames:
            s = STARTTLS(sslkwargs, local_hostname=local_hostname, host=mailhost)
        else:
            s = STARTTLS(sslkwargs, local_hostname=local_hostname)
    else:
        s = smtplib.SMTP(local_hostname=local_hostname)
    if smtps:
        defaultport = 465
    else:
        defaultport = 25
    mailport = util.getport(ui.config(b'smtp', b'port', defaultport))
    ui.note(_(b'sending mail: smtp host %s, port %d\n') %
            (mailhost, mailport))
    s.connect(host=mailhost, port=mailport)
    if starttls:
        ui.note(_(b'(using starttls)\n'))
        s.ehlo()
        s.starttls()
        s.ehlo()
    if starttls or smtps:
        if getattr(sslutil, 'validatesocket', None):
            ui.note(_(b'(verifying remote certificate)\n'))
            sslutil.validatesocket(s.sock)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    stored = password = password_store.get_smtp_password(
        mailhost, mailport, username)
    # No need to check whether password was found as try_smtp_login
    # just returns False if it is absent.
    while not try_smtp_login(ui, s, username, password):
        password = ui.getpass(_(b"Password for %s on %s:%d: ") % (username, mailhost, mailport))

    if stored != password:
        password_store.set_smtp_password(
            mailhost, mailport, username, password)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def send(sender, recipients, msg):
        try:
            return s.sendmail(sender, recipients, msg)
        except smtplib.SMTPRecipientsRefused as inst:
            recipients = [r[1] for r in inst.recipients.values()]
            raise error.Abort(b'\n' + b'\n'.join(recipients))
        except smtplib.SMTPException as inst:
            raise error.Abort(inst)

    return send

############################################################
# SMTP monkeypatching
############################################################


@monkeypatch_method(mail)
def _smtp(ui):
    """
    build an smtp connection and return a function to send email

    This is the monkeypatched version of _smtp(ui) function from
    mercurial/mail.py. It calls the original unless username
    without password is given in the configuration.
    """
    username = ui.config(b'smtp', b'username')
    password = ui.config(b'smtp', b'password')

    if username and not password:
        return keyring_supported_smtp(ui, username)
    else:
        return _smtp.orig(ui)


############################################################
# Custom commands
############################################################

cmdtable = {}
command = meu.command(cmdtable)


@command(b'keyring_check',
         [],
         _(b"keyring_check [PATH]"),
         optionalrepo=True)
def cmd_keyring_check(ui, repo, *path_args, **opts):   # pylint: disable=unused-argument
    """
    Prints basic info (whether password is currently saved, and how is
    it identified) for given path.

    Can be run without parameters to show status for all (current repository) paths which
    are HTTP-like.
    """
    defined_paths = [(name, url)
                     for name, url in ui.configitems(b'paths')]
    if path_args:
        # Maybe parameter is an alias
        defined_paths_dic = dict(defined_paths)
        paths = [(path_arg, defined_paths_dic.get(path_arg, path_arg))
                 for path_arg in path_args]
    else:
        if not repo:
            ui.status(meu.ui_string(b"Url to check not specified. Either run ``hg keyring_check https://...``, or run the command inside some repository (to test all defined paths).\n"))
            return
        paths = [(name, url) for name, url in defined_paths]

    if not paths:
        ui.status(meu.ui_string(b"keyring_check: no paths defined\n"))
        return

    handler = HTTPPasswordHandler()

    ui.status(meu.ui_string(b"keyring password save status:\n"))
    for name, url in paths:
        if not is_http_path(url):
            if path_args:
                ui.status(meu.ui_string(b"    %s: non-http path (%s)\n",
                                        name, url))
            continue
        user, pwd, source, final_url = handler.get_credentials(
            make_passwordmgr(ui), name, url)
        if pwd:
            ui.status(meu.ui_string(
                b"    %s: password available, source: %s, bound to user %s, url %s\n",
                name, source, user, final_url))
        elif user:
            ui.status(meu.ui_string(
                b"    %s: password not available, once entered, will be bound to user %s, url %s\n",
                name, user, final_url))
        else:
            ui.status(meu.ui_string(
                b"    %s: password not available, user unknown, url %s\n",
                name, final_url))


@command(b'keyring_clear',
         [],
         _(b'hg keyring_clear PATH-OR-ALIAS'),
         optionalrepo=True)
def cmd_keyring_clear(ui, repo, path, **opts):  # pylint: disable=unused-argument
    """
    Drops password bound to given path (if any is saved).

    Parameter can be given as full url (``https://John@bitbucket.org``) or as the name
    of path alias (``bitbucket``).
    """
    path_url = path
    for name, url in ui.configitems(b'paths'):
        if name == path:
            path_url = url
            break
    if not is_http_path(path_url):
        ui.status(meu.ui_string(
            b"%s is not a http path (and %s can't be resolved as path alias)\n",
            path, path_url))
        return

    handler = HTTPPasswordHandler()

    user, pwd, source, final_url = handler.get_credentials(
        make_passwordmgr(ui), path, path_url)
    if not user:
        ui.status(meu.ui_string(b"Username not configured for url %s\n",
                                final_url))
        return
    if not pwd:
        ui.status(meu.ui_string(b"No password is saved for user %s, url %s\n",
                                user, final_url))
        return

    if source != handler.SRC_KEYRING:
        ui.status(meu.ui_string(b"Password for user %s, url %s is saved in %s, not in keyring\n",
                                user, final_url, source))

    password_store.clear_http_password(final_url, user)
    ui.status(meu.ui_string(b"Password removed for user %s, url %s\n",
                            user, final_url))


buglink = b'https://foss.heptapod.net/mercurial/mercurial_keyring/issues'
