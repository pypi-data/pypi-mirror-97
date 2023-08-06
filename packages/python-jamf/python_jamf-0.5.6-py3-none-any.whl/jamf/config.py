# -*- coding: utf-8 -*-

"""
Configuration for jamfutil
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2020 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "1.2.4"

import copy
import getpass
import logging
import plistlib
import itertools
import keyring
from os import path, remove
LINUX_PREFS_TILDA = '~/.edu.utah.mlib.jamfutil.plist'
MACOS_PREFS_TILDA = '~/Library/Preferences/edu.utah.mlib.jamfutil.plist'
AUTOPKG_PREFS_TILDA = '~/Library/Preferences/com.github.autopkg.plist'
JAMF_PREFS = '/Library/Preferences/com.jamfsoftware.jamf.plist'
MAGIC = (125, 137, 82, 35, 210, 188, 221, 234, 163, 185, 31)
logging.getLogger(__name__).addHandler(logging.NullHandler())


class Error(Exception):
    pass


class CorruptedConfigError(Error):
    pass


class ValidationError(Error):
    pass


class Config:
    def __init__(self,
                 config_path=None,
                 hostname=None,
                 username=None,
                 password=None,
                 prompt=False,
                 explain=False):
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.prompt = prompt
        self.hostname = hostname
        self.username = username
        self.password = password
        if not self.hostname and not self.username and not self.password:
            macos_prefs = path.expanduser(MACOS_PREFS_TILDA)
            if not config_path:
                linux_prefs = path.expanduser(LINUX_PREFS_TILDA)
                autopkg_prefs = path.expanduser(AUTOPKG_PREFS_TILDA)
                if path.exists(macos_prefs):
                    if explain:
                        print("Using "+macos_prefs)
                    config_path = macos_prefs
                elif path.exists(linux_prefs):
                    if explain:
                        print("Using "+linux_prefs)
                    config_path = linux_prefs
                elif path.exists(autopkg_prefs):
                    if explain:
                        print("Using "+autopkg_prefs)
                    config_path = autopkg_prefs
                elif path.exists(JAMF_PREFS):
                    if explain:
                        print("Using "+JAMF_PREFS)
                    config_path = JAMF_PREFS
                else:
                    if explain:
                        print("Using "+macos_prefs+" but it doesn't exist yet.")
                    config_path = macos_prefs
            elif explain:
                    print("Using "+config_path+" because you said so.")

            if config_path[0] == '~':
                config_path = path.expanduser(config_path)
                if explain:
                    print("Expanding the path. Using "+config_path)

            if not self.hostname and not self.username and not self.password:
                if path.exists(config_path):
                    fptr = open(config_path, 'rb')
                    prefs = plistlib.load(fptr)
                    fptr.close()
                    if 'JSSHostname' in prefs:
                        if 'Credentials' in prefs:
                            print("Please delete the prefs "+config_path+" "
                                  "and recreate them (format has changed).")
                            exit(1)
                        self.hostname = prefs['JSSHostname']
                        self.username = prefs['Username']
                        self.password = keyring.get_password(self.hostname,
                                                             self.username)
                    elif 'JSS_URL' in prefs:
                        self.hostname = prefs["JSS_URL"]
                        self.username = prefs["API_USERNAME"]
                        self.password = prefs["API_PASSWORD"]
                    elif 'jss_url' in prefs:
                        self.hostname = prefs["jss_url"]
                        # No auth in that file
                else:
                    self.log.debug(f"file not found: {config_path}")

        # Prompt for any missing prefs
        if self.prompt:
            if not self.hostname:
                self.hostname = prompt_hostname()
            if not self.username:
                self.username = input("username: ")
            if not self.password:
                self.password = getpass.getpass()
        elif not self.hostname and not self.username and not self.password:
            print("No jamf config file could be found and prompt is off.")
            exit(1)

    def save(self, config_path=None):
        keyring.set_password(self.hostname, self.username, self.password)
        data = {
            'JSSHostname': self.hostname,
            'Username': self.username
        }
        self.log.info(f"saving: {config_path}")
        fptr = open(config_path, 'wb')
        plistlib.dump(data, fptr)
        fptr.close()

    def reset(self, path):
        keyring.delete_password(self.hostname, self.username)
        remove(path)


def prompt_hostname():
    return input('Hostname (don\'t forget https:// and :8443): ')
