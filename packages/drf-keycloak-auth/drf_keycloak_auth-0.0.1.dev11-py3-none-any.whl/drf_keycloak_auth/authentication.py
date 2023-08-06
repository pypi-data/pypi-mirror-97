""" add a keycloak authentication class specific to Django Rest Framework """
from typing import Tuple, Dict
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser, update_last_login
from django.contrib.auth import get_user_model
from rest_framework import (
    authentication,
    exceptions,
)

from .keycloak import keycloak_openid
from .settings import api_settings
from . import __title__

log = logging.getLogger(__title__)
User = get_user_model()


class KeycloakAuthentication(authentication.TokenAuthentication):
    keyword = api_settings.KEYCLOAK_AUTH_HEADER_PREFIX

    def authenticate_credentials(
        self,
        token: str
    ) -> Tuple[AnonymousUser, Dict]:
        """ Attempt to verify JWT from Authorization header with Keycloak """
        log.debug('KeycloakAuthentication.authenticate_credentials')
        try:
            user = None
            # Checks token is active
            decoded_token = keycloak_openid.introspect(token)
            is_active = decoded_token.get('active', False)
            if not is_active:
                raise exceptions.AuthenticationFailed(
                    'invalid or expired token'
                )
            if api_settings.KEYCLOAK_MANAGE_LOCAL_USER is not True:
                log.info(
                    'KeycloakAuthentication.authenticate_credentials: '
                    f'{decoded_token}'
                )
                user = AnonymousUser()
            else:
                django_fields = {}
                keycloak_username_field = \
                    api_settings.KEYCLOAK_FIELD_AS_DJANGO_USERNAME

                sub = decoded_token['sub']
                if keycloak_username_field and type(keycloak_username_field) is str:
                    django_fields['username'] = \
                        decoded_token.get(keycloak_username_field, '')
                django_fields['email'] = decoded_token.get('email', '')
                # django stores first_name and last_name as empty strings
                # by default, not None
                django_fields['first_name'] = decoded_token.get('given_name', '')
                django_fields['last_name'] = decoded_token.get('family_name', '')
                try:
                    user = User.objects.get(pk=sub)
                    # user_values = (user.email, user.first_name, user.last_name,)
                    # token_values = (email, first_name, last_name,)
                    save_model = False

                    for key, value in django_fields.items():
                        try:
                            if getattr(user, key) != value:
                                setattr(user, key, value)
                                save_model = True
                        except Exception:
                            log.warn(
                                'KeycloakAuthentication.'
                                'authenticate_credentials - '
                                f'setattr: {key} field does not exist'
                            )
                    if save_model:
                        user.save()
                except ObjectDoesNotExist:
                    log.warn(
                        'KeycloakAuthentication.authenticate_credentials - '
                        f'ObjectDoesNotExist: {sub} does not exist'
                    )

                if user is None:
                    django_fields.update({'pk': sub})
                    user = User.objects.create_user(**django_fields)

                update_last_login(sender=None, user=user)

            log.info(
                'KeycloakAuthentication.authenticate_credentials: '
                f'{user} - {decoded_token}'
            )
            return (user, decoded_token)
        except Exception as e:
            log.error(
                'KeycloakAuthentication.authenticate_credentials - '
                f'Exception: {e}'
            )
            raise exceptions.AuthenticationFailed()
