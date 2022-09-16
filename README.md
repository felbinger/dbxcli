# felbinger/dbxcli

[dropbox/dbxcli](https://github.com/dropbox/dbxcli) with support for refresh tokens (workarround using python) and custom app.

## Install
```bash
sudo mkdir -p /usr/share/dbxcli
sudo git clone https://github.com/felbinger/dbxcli.git /usr/share/dbxcli
# if nessesary, adjust app key and secret in /usr/share/dbxcli/dbxcli.sh
# adjust refresh_token in /usr/share/dbxcli/.check_access_token.py
sudo ln -s /usr/share/dbxcli/dbxcli.sh /usr/local/bin/dbxcli
```
