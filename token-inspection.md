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
