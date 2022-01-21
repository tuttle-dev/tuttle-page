"""Cloud connectors."""

import getpass
import pyicloud

from .model import ICloudAccount, GoogleAccount


def login_iCloud(account: ICloudAccount):
    """Log in to Apple iCloud"""
    user_name = account.user_name
    password = getpass.getpass(
        prompt=f"iCloud password for account {account.user_name}: "
    )
    iCloud = pyicloud.PyiCloudService(user_name, password)
    if not iCloud.is_trusted_session:
        result = iCloud.validate_2fa_code(getpass.getpass(prompt="verification code: "))
    assert iCloud.is_trusted_session
    return iCloud


def login_google(account: GoogleAccount):
    """Log into Google API."""
    # TODO:
    raise NotImplementedError("TODO")
