from mozilla_django_oidc.auth import OIDCAuthenticationBackend
import requests

from josepy.b64 import b64decode
from josepy.jwk import JWK
from josepy.jws import JWS, Header
from django.utils.encoding import force_bytes, smart_text, smart_bytes
class OIDCbackend(OIDCAuthenticationBackend):
    def get_username(self, claims):
        print('local')
        print(claims)
        return claims.get('preferred_username')

    # def get_token(self, payload):
    #     """Return token object as a dictionary."""
    #     print('getting tken')
    #     auth = None
    #     if self.get_settings('OIDC_TOKEN_USE_BASIC_AUTH', False):
    #         # When Basic auth is defined, create the Auth Header and remove secret from payload.
    #         user = payload.get('client_id')
    #         pw = payload.get('client_secret')

    #         auth = HTTPBasicAuth(user, pw)
    #         del payload['client_secret']

    #     response = requests.post(
    #         'http://stackn-keycloak-http/auth/realms/STACKn/protocol/openid-connect/token',
    #         data=payload,
    #         auth=auth,
    #         verify=False, #self.get_settings('OIDC_VERIFY_SSL', True),
    #         timeout=self.get_settings('OIDC_TIMEOUT', None),
    #         proxies=self.get_settings('OIDC_PROXY', None))
    #     response.raise_for_status()
    #     return response.json()

    # def retrieve_matching_jwk(self, token):
    #     """Get the signing key by exploring the JWKS endpoint of the OP."""
    #     response_jwks = requests.get(
    #         'http://stackn-keycloak-http/auth/realms/STACKn/protocol/openid-connect/certs',
    #         verify=False,
    #         timeout=self.get_settings('OIDC_TIMEOUT', None),
    #         proxies=self.get_settings('OIDC_PROXY', None)
    #     )
    #     response_jwks.raise_for_status()
    #     jwks = response_jwks.json()

    #     # Compute the current header from the given token to find a match
    #     jws = JWS.from_compact(token)
    #     json_header = jws.signature.protected
    #     header = Header.json_loads(json_header)

    #     key = None
    #     for jwk in jwks['keys']:
    #         if jwk['kid'] != smart_text(header.kid):
    #             continue
    #         if 'alg' in jwk and jwk['alg'] != smart_text(header.alg):
    #             continue
    #         key = jwk
    #     if key is None:
    #         raise SuspiciousOperation('Could not find a valid JWKS.')
    #     return key