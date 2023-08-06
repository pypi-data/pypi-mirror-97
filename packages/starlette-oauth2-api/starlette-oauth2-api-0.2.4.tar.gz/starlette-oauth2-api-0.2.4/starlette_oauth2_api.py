import urllib.request, json
import logging
import typing

import jose.jwt
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


logger = logging.getLogger(__name__)


def _get_keys(url_or_keys):
    if isinstance(url_or_keys, str) and url_or_keys.startswith('https://'):
        logger.info("Getting jwk from %s...", url_or_keys)
        with urllib.request.urlopen(url_or_keys) as f:
            return json.loads(f.read().decode())
    else:
        return url_or_keys


class InvalidToken(Exception):
    """When a token is invalid for all identity providers"""
    def __init__(self, errors):
        self.errors = errors


def _validate_provider(provider_name, provider):
    mandatory_keys = {'issuer', 'keys', 'audience'}
    if not mandatory_keys.issubset(set(provider)):
        raise ValueError(f'Each provider must contain the following keys: {mandatory_keys}. Provider "{provider_name}" is missing {mandatory_keys - set(provider)}.')

    keys = provider['keys']
    if isinstance(keys, str) and keys.startswith('http://'):
        raise ValueError(f'When "keys" is a url, it must start with "https://". This is not true in the provider "{provider_name}"')


class AuthenticateMiddleware:
    """
    A starlette middleware to authenticate and authorize requests through OAuth2 JWT tokens.

    Use ``public_paths`` to add paths that do not require authentication, e.g. `/public-endpoint`.
    Every route that is not a public path returns 401 if it does not have an authorization header with `Bearer {token}` where token is a valid jwt.

    ``providers`` must be a dictionary with the following keys:
        * ``uri``: a uri of the openid-configuration
        * ``issuer``: issuer or the tokens
        * ``audience``: audience or the tokens

    If multiple providers are passed, the request is valid if any of the providers authenticates the request.
    """
    def __init__(self, app: ASGIApp, providers, public_paths=None, get_keys=None) -> None:
        self._app = app
        for provider in providers:
            _validate_provider(provider, providers[provider])
        self._providers = providers
        self._get_keys = get_keys or _get_keys
        self._public_paths = public_paths or set()

        # cached attribute
        self._keys = {}

    def _provider_claims(self, provider, token):
        """
        Validates the token and returns its respective claims against a specific provider.

        The ``at_hash`` value in the token, if present, is ignored, because in order to
        verify it, the access token would be required, which we don't have access to.
        """
        issuer = self._providers[provider]['issuer']
        audience = self._providers[provider]['audience']
        logger.debug("Trying to decode token for provider \"%s\", issuer \"%s\", audience \"%s\"...", provider, issuer, audience)
        decoded = jose.jwt.decode(
            token, self._provider_keys(provider),
            issuer=issuer,
            audience=audience,
            options={'verify_at_hash': False}  # Ignore at_hash, if present
        )
        logger.debug("Token decoded.")
        return decoded

    def claims(self, token: str) -> typing.Tuple[str, typing.Dict[str, str]]:
        """
        Validates the token and returns its respective claims. The token can be any of the valid providers declared 
        for this middleware.
        """
        errors = {}
        for provider in self._providers:
            try:
                return provider, self._provider_claims(provider, token)
            except jose.exceptions.ExpiredSignatureError as e:
                # if the token has expired, it is at least from this provider.
                logger.debug("Token has expired.")
                errors = str(e)
                break
            except jose.exceptions.JWTClaimsError as e:
                logger.debug("Invalid claims")
                errors[provider] = str(e)
            except jose.exceptions.JOSEError as e:  # the catch-all of Jose
                logger.warning(e, exc_info=True)
                errors[provider] = str(e)
        raise InvalidToken(errors)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope)

        if request.url.path in self._public_paths:
            return await self._app(scope, receive, send)

        # check for authorization header and token on it.
        if 'authorization' in request.headers and request.headers['authorization'].startswith('Bearer '):
            token = request.headers['authorization'][len('Bearer '):]
            try:
                provider, claims = self.claims(token)
                scope['oauth2-claims'] = claims
                scope['oauth2-provider'] = provider
            except InvalidToken as e:
                response = JSONResponse({'message': e.errors}, status_code=401)
                return await response(scope, receive, send)
        elif 'authorization' in request.headers:
            logger.debug("No \"Bearer\" in authorization header")
            response = JSONResponse({'message': 'The "authorization" header must start with "Bearer "'}, status_code=400)
            return await response(scope, receive, send)
        else:
            logger.debug("No authorization header")
            response = JSONResponse({'message': 'The request does not contain an "authorization" header'}, status_code=400)
            return await response(scope, receive, send)

        return await self._app(scope, receive, send)

    def _provider_keys(self, provider: str):
        """
        Returns the jw keys of the provider. This is retrieved from the internet and cached at the first retrieval.
        """
        if self._keys.get(provider, None) is None:
            self._keys[provider] = self._get_keys(self._providers[provider]['keys'])
        return self._keys[provider]
