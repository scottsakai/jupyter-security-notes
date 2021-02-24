#!/usr/bin/env python3

import sys
import requests
import configparser


# read in the config
# moved to a config file so we never accidentally check in secrets
config = configparser.ConfigParser()
config.read('/dev/shm/globusauth.ini')
globusconf = config['globus']

# https://docs.globus.org/api/auth/developer-guide/#register-app
SERVICE_CLIENT_ID = globusconf.get('SERVICE_CLIENT_ID')
SERVICE_CLIENT_SECRET = globusconf.get('SERVICE_CLIENT_SECRET')

# https://docs.globus.org/api/auth/reference/#token-introspect
INTROSPECTION_URL = globusconf.get('INTROSPECTION_URL', 'https://auth.globus.org/v2/oauth2/token/introspect')

# Required identity provider domain to get the username from
IDENTITY_PROVIDER = globusconf.get('IDENTITY_PROVIDER')

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
        return identity['username']
    else:
        return None

if __name__ == '__main__':
    sys.stderr.write("Access Token:\n")
    token = input()

    try:
        username = check_token(token.rstrip())
    except:
        sys.exit(1)

    if username:
        print(username)
        sys.exit(0)
    else:
        sys.exit(1)
