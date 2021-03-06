"""Provide the Auth class."""
from prawcore import ImplicitAuthorizer, UntrustedAuthenticator, session

from .base import PRAWBase
from ..exceptions import ClientException


class Auth(PRAWBase):
    """Auth provides an interface to Reddit's authorization."""

    def implicit(self, access_token, expires_in, scope):
        """Set the active authorization to be an implicit authorization.

        :param access_token: The access_token obtained from Reddit's callback.
        :param expires_in: The number of seconds the ``access_token`` is valid
            for. The origin of this value was returned from Reddit's callback.
            You may need to subtract an offset before passing in this number to
            account for a delay between when Reddit prepared the response, and
            when you make this function call.
        :param scope: A space-delimited string of Reddit OAuth2 scope names as
            returned from Reddit's callback.

        Raise ``ClientException`` if ``Reddit`` was initialized for a
        non-installed application type.

        """
        authenticator = self._reddit._read_only_core._authorizer._authenticator
        if not isinstance(authenticator, UntrustedAuthenticator):
            raise ClientException('implicit can only be used with installed '
                                  'apps.')
        implicit_session = session(ImplicitAuthorizer(
            authenticator, access_token, expires_in, scope))
        self._reddit._core = self._reddit._authorized_core = implicit_session

    def url(self, scopes, state, duration='permanent'):
        """Return the URL used out-of-band to grant access to your application.

        :param scopes: A list of OAuth scopes to request authorization for.
        :param state: A string that will be reflected in the callback to
            ``redirect_uri``. This value should be temporarily unique to the
            client for whom the URL was generated for.
        :param duration: (web app only) Either ``permanent`` or ``temporary``
            (default: permanent). ``temporary`` authorizations generate access
            tokens that last only 1 hour. ``permanent`` authorizations
            additionally generate a refresh token that can be indefinitely used
            to generate new hour-long access tokens. This value is ignored for
            installed apps as only temporary tokens can be generated for them.

        """
        authenticator = self._reddit._read_only_core._authorizer._authenticator
        if isinstance(authenticator, UntrustedAuthenticator):
            return authenticator.authorize_url(scopes, state)
        raise ClientException('url is not yet supported for web app')
