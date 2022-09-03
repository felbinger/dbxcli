#!/usr/bin/env python3

import json
import datetime
from dropbox import Dropbox, DropboxOAuth2FlowNoRedirect
from os import environ


def _authenticate(api_key: str, api_secret: str) -> str:
    auth_flow = DropboxOAuth2FlowNoRedirect(api_key, consumer_secret=api_secret, token_access_type='offline')

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)
    return oauth_result.refresh_token


def check_and_refresh_access_token(api_key: str, api_secret: str, access_token: str, refresh_token: str = None, exp: datetime = None):
    if not refresh_token:
        refresh_token = _authenticate(api_key, api_secret)

    with Dropbox(oauth2_refresh_token=refresh_token, oauth2_access_token=access_token, oauth2_access_token_expiration=exp, app_key=api_key, app_secret=api_secret) as dbx:
        dbx.check_and_refresh_access_token()
        return dbx._oauth2_access_token, dbx._oauth2_access_token_expiration


def _get_dbxcli_config(auth_filename: str = "/root/.config/dbxcli/auth.json"):
    with open(auth_filename, 'r') as f:
        return json.load(f)


def _set_dbxcli_config(config: str, auth_filename: str = "/root/.config/dbxcli/auth.json"):
    with open(auth_filename, 'w') as f:
        # write new access token in config file for dbxcli
        json.dump(config, f)


if __name__ == "__main__":
    content = _get_dbxcli_config()

    # extract access token from dbxcli config
    access_token = content.get("").get("personal")
    exp = datetime.datetime.fromisoformat(content.get("").get("expired"))

    # check if the access token is still valid
    returned_access_token, returned_exp = check_and_refresh_access_token(
      api_key=environ.get("DROPBOX_PERSONAL_APP_KEY", ""),
      api_secret=environ.get("DROPBOX_PERSONAL_APP_SECRET", ""),
      access_token=access_token,
      refresh_token="YOUR_REFRESH_TOKEN_GOES_HERE",
      exp=exp
    )

    # in case the old access token is invalid
    if access_token != returned_access_token:
        content[""]["personal"] = returned_access_token
        content[""]["expired"] = returned_exp.isoformat()
        _set_dbxcli_config(content)
