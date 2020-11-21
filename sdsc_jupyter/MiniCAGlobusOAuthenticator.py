import os
from traitlets import Unicode
from oauthenticator.globus import LocalGlobusOAuthenticator

# to do
# subclass GlobusOAuthenticator
# overload authenticate and pre_spawn_hook calls
# call them, then add steps to get sign certs

class MiniCAGlobusOAuthenticator(LocalGlobusOAuthenticator):
    mini_ca_scope = Unicode(
        help="""Scope for the token sent to the Mini CA.""").tag(config=True)

    def _mini_ca_scope_default(self):
        return os.getenv('MINI_CA_SCOPE', '')

    async def authenticate(self, handler, data=None):
        if not self.mini_ca_scope in self.scope:
            self.scope.append(self.mini_ca_scope)
        user_info = await super().authenticate(handler, data=data)
        return user_info
