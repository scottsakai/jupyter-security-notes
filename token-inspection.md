# Introspecting Globus OAuth Access Tokens

Globus uses [RFC 7662 OAuth 2.0 Token
Introspection](https://tools.ietf.org/html/rfc7662) for resource
servers to get information about an access token. The
resouce server `POST`s the token to the introspection endpoint
(URL). If the resource server is authorized to introspect that token,
Globus Auth will respond with information like if the token is active,
the client it was issued to, if asked for, the identity of the account (user).

Getting this working only takes a few steps:

1. [Registering a Globus Auth client application](https://docs.globus.org/api/auth/developer-guide/#register-app)
2. (Optional) Verify [an FQDN for the client](https://docs.globus.org/api/auth/reference/#add_fqdn)
3. [Create one or more scopes owned by the client](https://docs.globus.org/api/auth/reference/#create_scope)
4. Requesting tokens with the new scope
5. [Introspecting a token](https://docs.globus.org/api/auth/reference/#token-introspect)

There are several scripts here to help get this set up.

* [`createscope.py`](createscope.py)
* [`gettoken.py`](gettoken.py)
* [`minicatokencheck.py`](minicatokencheck.py)

## Quick How-To

Go to the [Globus Developers page](https://developers.globus.org) and follow the steps in the Globus Developer Guide for [application registration](https://docs.globus.org/api/auth/developer-guide/#register-app). Do not select Native App, and for the redirect URL you can put in something like `http://localhost:5000`. There's no need for a redirect URL for this application since it won't be used for authentication via OIDC. When you're done registering your application, you should have a client ID and a client secret.

If you want to verify an FQDN for your client or resource server, you'll need to add a NDS TXT record for a host you manage.

Update the [`createscope.py`](createscope.py) and [`minicatokencheck.py`](minicatokencheck.py) scripts with the client ID and secret, the optional FQDN, and name, description, and short name for the scope. Run [`createscope.py`](createscope.py) and cross your fingers. At the end you should see the information about your client. You can remove the FQDN and scope settings and re-run the script at any time to get the client info.

Try [`gettoken.py`](gettoken.py) script to get an access for your new scope. If you specified the FQDN, your scope will be `https://auth.globus.org/scopes/<fqdn>/<scope short name>`. Otherwise, it will be `https://auth.globus.org/scopes/<CLIENT_ID>/<scope short name>`. 

Here's an example
```
$ ./gettoken.py https://auth.globus.org/scopes/batchtest2.jupyter-security.info/minica
<opaque token string>
```

Once you have an access token, you can pass it to the [`minicatokencheck.py`](minicatokencheck.py) script to see if it's valid and if the user has an identity from a domain you trust. The token checking code is what you'll put on your resource server to make decisions about authorizing users based on the tokens received.

```
$ ./minicatokencheck.py <good opaque token string>
rpwagner
$ ./minicatokencheck.py <bad opaque token string>
$ echo $?
1
```
