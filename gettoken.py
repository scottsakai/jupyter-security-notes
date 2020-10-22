#!/usr/bin/env python

import sys
from fair_research_login import NativeClient

# This is a minimal Globus Auth Native App that returns an access token
#
# It uses the FAIR Research Login package to do the work
# pip install fair-research-login

CLIENT_ID = 'd719c82f-3a11-4de1-9d87-d52d28ec31b6'

# Be careful with enabling refresh tokens, they can leave a long-lived
# mechanism to retrieve access on your system
REFRESH_TOKENS = False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ./gettoken.py <scope>')
        print('Example: ./gettoken.py openid')
        sys.exit(1)

    scope = sys.argv[1]
    cli = NativeClient(client_id=CLIENT_ID,
                           default_scopes=[scope,])
    try:
        tokens = cli.load_tokens_by_scope(requested_scopes=[scope,])
    except:
        cli.login(requested_scopes=[scope,],
                      refresh_tokens=REFRESH_TOKENS)
        tokens = cli.load_tokens_by_scope(requested_scopes=[scope,])

    print(tokens[scope]['access_token'])
