#!/bin/bash

export DROPBOX_PERSONAL_APP_KEY=tep71hp5zuei89a
export DROPBOX_PERSONAL_APP_SECRET=ntsyut8ljj29fbw

/usr/share/dbxcli/.check_access_token.py
/usr/share/dbxcli/.dbxcli-linux-amd64 "${@}"
