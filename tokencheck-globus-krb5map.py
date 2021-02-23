#!/usr/bin/env python3

import sys
import requests
import configparser
from bsddb3 import db
import re


# read in the config
# moved to a config file so we never accidentally check in secrets
config = configparser.ConfigParser()
config.read('/var/secrets/globusauth.ini')
globusconf = config['globus']

# https://docs.globus.org/api/auth/developer-guide/#register-app
SERVICE_CLIENT_ID = globusconf.get('SERVICE_CLIENT_ID')
SERVICE_CLIENT_SECRET = globusconf.get('SERVICE_CLIENT_SECRET')

# https://docs.globus.org/api/auth/reference/#token-introspect
INTROSPECTION_URL = globusconf.get('INTROSPECTION_URL', 'https://auth.globus.org/v2/oauth2/token/introspect')

# Required identity provider domain to get the username from
IDENTITY_PROVIDER = globusconf.get('IDENTITY_PROVIDER')

# BSD DB map file (kerberos principals to localname)
BDB_MAPFILE = globusconf.get('BDB_MAPFILE')


# we need to map a federated identity to a local identity
# the existing berkeley db files used for kerberos authentication
# should work nicely.
# load that up now so it blows up before token handling.
bdbmap = db.DB()
bdbmap.open(BDB_MAPFILE, flags=db.DB_RDONLY)

def map_to_local(federated_id):
    # maps federated id to local id
    # for XSEDE identities,  an @xsede.org should first be substituted
    # to @TERAGRID.ORG due to the continued use of the TERAGRID.ORG kerberos 
    # realm.
    federated_id = re.sub('@xsede\.org$', "@TERAGRID.ORG", federated_id, 1)

    # the db is all binary, which means our keys and values are null-terminated
    # make sure there's a null, else nothing matches!
    federated_id += "\x00"
    bytekey = federated_id.encode() 

    if not bdbmap[bytekey]:
        return None

    # remember to turn bytes into string!
    local_id = bdbmap[bytekey].decode()
    local_id = re.sub("\x00", "", local_id)
    return local_id


def check_token(access_token):
    # Calls the Globus RFC 7662 OAuth 2.0 Token Introspection URL
    # Returns a username if the token is active and
    # an identity is found with the specifified IdP
    # Otherwise, returns None
    resp = requests.post(
        INTROSPECTION_URL,
        data={'token': access_token, 'include': 'identity_set_detail'},
        auth=(SERVICE_CLIENT_ID, SERVICE_CLIENT_SECRET),
        verify=True)
    resp_dict = resp.json()
    if not resp_dict['active']:
        return None
    has_desired_idp = False
    for identity in resp_dict['identity_set_detail']:
        username, domain = identity['username'].split('@', 1)
        if domain == IDENTITY_PROVIDER:
            has_desired_idp = True
            break
    if has_desired_idp:
        return map_to_local(identity['username'])
    else:
        return None

if __name__ == '__main__':
    sys.stderr.write("Access Token:\n")
    token = input()

    try:
        username = check_token(token.rstrip())
    # note: this except will catch a sys.exit!
    except:
        sys.exit(1)

    if username:
        print(username)
        sys.exit(0)
    else:
        sys.exit(1)
