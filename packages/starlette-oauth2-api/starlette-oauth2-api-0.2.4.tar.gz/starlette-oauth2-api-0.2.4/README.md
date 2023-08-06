[![pipeline status](https://gitlab.com/jorgecarleitao/Starlette-oauth2-api/badges/master/pipeline.svg)](https://gitlab.com/jorgecarleitao/Starlette-oauth2-api/commits/master)
[![coverage report](https://gitlab.com/jorgecarleitao/Starlette-oauth2-api/badges/master/coverage.svg)](https://gitlab.com/jorgecarleitao/Starlette-oauth2-api/commits/master)

# Starlette OAuth2

A Starlette middleware for authentication and authorization through JWT.

This middleware is intended to add authentication and authorization to an API (e.g. FastAPI) through access tokens provided by an external auth provider (e.g. Microsoft AD, Auth0).
Its main use-case is when you have an API that relies on an external identity provider for authentication and authorization, and whose clients can request access tokens themselves. In this case, the API does not need to communicate with the identity provider - it only needs to validate that the access tokens are signed by the identity provider.

This middleware depends only on `python-jose`, which it uses to decode and validate JWTs.

## How to install

```
pip install starlette-oauth2-api
```

## How to use

Below is an example of how to use this middleware:

```
from starlette.applications import Starlette
from starlette_oauth2_api import AuthenticateMiddleware


app = Starlette()
app.add_middleware(AuthenticateMiddleware,
    providers={
        'google': {
            'keys': 'https://www.googleapis.com/oauth2/v3/certs',
            'issuer': 'https://accounts.google.com',
            'audience': '852159111111-xxxxxx.apps.googleusercontent.com',
        }
    },
    public_paths={'/'},
)
```

At this point, every route except `/` requires an `authorization: Bearer {token}` where `token` must:

* be a JWT
* be issued by `issuer` to the audience `audience`
* be signed by one of the keys in `https://www.googleapis.com/oauth2/v3/certs`
* not have expired

Failing any of the conditions above returns a 401 response, failing to contain the header with `Bearer ` returns a 400 response.

When the request is valid, the Middlware adds all claims in the JWT to `oauth2-claims`, which can be accessed using

```
...
def home(request):
    ...
    request.scope['oauth2-claims']
    ...
```

In particular, if your identity provider provides custom claims, you can use these for authorization.

## Details

The argument `providers` must be a dictionary whose keys are arbitrary, and its values must be a dictionary containing three keys:

* `issuer`
* `audience`
* `keys`

#### Issuer (iss)

This middleware uses the issuer to validate (by python-Jose) that the token was issued by a specific entity. Examples of issuers:

* Microsoft: `https://login.microsoftonline.com/<ad_tenant_id>/v2.0`
* Google: `https://accounts.google.com`

This value can be found at `https://.../.well-known/openid-configuration`, key `iss`.

#### Audience (aud)

Like the issuer, this middleware uses the audience to validate that the token was intended for this API.
Some examples of audiences from out-there:

* Microsoft: `https://<app-name>.azurewebsites.net`
* Google: `<tenant>-<project>.apps.googleusercontent.com`

This value can be found when the application is configured in AD, which depends on the particular Identity
provider that you use.

#### Keys (jwks)

`keys` correspond to the public keys of the identity provider, whose corresponding (private) counterpart was used to sign the token. This middleware relies on Python-Jose to verify that the token was signed by the counterpart key of this field.

`keys` can be a URL another object. When it is a URL, this middleware fetches the keys from it. Examples:

* Microsoft: `https://login.microsoftonline.com/<tenant-id>/discovery/v2.0/keys`
* Google: `https://www.googleapis.com/oauth2/v3/certs`

This URL can be found at `https://.../.well-known/openid-configuration`, key `jwks_uri`.

When `keys` is another object, it represents a JWK, JWK set as per RFC 7517, or other (non-standard) variation that python-jose accepts. An example of its content:

```
{'keys': [
    {
        "kid": "...",
        "e": "AQAB",
        "kty": "RSA",
        "alg": "RS256",
        "n": "...",
        "use": "sig"
    },
]}
```

The tradeoff between providing a JWK set or a url is the following: on the one hand, if you provide a JWK set, this middleware does not need access to the public internet to validate tokens, and can thus be deployed on environments without it. On the other hand, JWK are eventually rotated by the
identity provider and you will have redeploy the application with the respective updated public keys.

#### Decoding

The signature is verified with the keys explained above. If the token carries an `at_hash` key in it's payload, it will be ignored. This is because the access token is required to decode it, which we do not have access to.
