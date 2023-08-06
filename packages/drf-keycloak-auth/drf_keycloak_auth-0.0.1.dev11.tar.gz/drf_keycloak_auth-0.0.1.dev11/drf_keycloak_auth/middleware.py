import logging
from typing import List

from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from .keycloak import get_resource_roles, add_role_prefix
from . import __title__
from .settings import api_settings

log = logging.getLogger(__title__)

User = get_user_model()


class KeycloakMiddleware:

    def __init__(self, get_response):     
        # Django response
        self.get_response = get_response

    def __call__(self, request):
        log.debug('KeycloakMiddleware.__call__')
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs) -> None:
        """
        middleware lifecyle method where view has been determined
        
        SimpleLazyObject required as KeycloakMiddleware is called BEFORE
        KeycloakAuthentication
        """
        log.debug('KeycloakMiddleware.process_view')
        request.roles = SimpleLazyObject(lambda: self._bind_roles_to_request(request))
        log.debug('KeycloakMiddleware.process_view complete')

    def _bind_roles_to_request(self, request) -> List[str]:
        """ try to add roles from authenticated keycloak user """
        roles = []
        try:
            roles += get_resource_roles(request.auth)
            roles.append(str(request.user.pk))
        except Exception as e:
            log.warn(
                f'KeycloakMiddleware._bind_roles_to_request - Exception: {e}'
            )

        if api_settings.KEYCLOAK_MANAGE_LOCAL_GROUPS is True:
            groups = self._get_or_create_groups(roles)
            self._refresh_user_groups(request, groups)

        self._user_is_staff(request, roles)

        log.info(f'KeycloakMiddleware.bind_roles_to_request: {roles}')
        return roles

    def _user_is_staff(self, request, roles: List[str]) -> None:
        """
        toggle user.is_staff if a role mapping has been declared in settings
        """
        try:
            user = request.user
            # catch None or django.contrib.auth.models.AnonymousUser
            valid_user = bool(
                user
                and type(user) is User
                and hasattr(user, 'is_staff')
                and getattr(user, 'is_superuser', False) is False
            )
            log.info(
                f'KeycloakMiddleware._user_is_staff - {user} - valid_user: '
                f'{valid_user}'
            )
            if (
                valid_user
                and api_settings.KEYCLOAK_ROLES_TO_DJANGO_IS_STAFF
                and type(api_settings.KEYCLOAK_ROLES_TO_DJANGO_IS_STAFF)
                in [list, tuple, set]
            ):
                is_staff_roles = set(
                    add_role_prefix(
                        api_settings.KEYCLOAK_ROLES_TO_DJANGO_IS_STAFF
                    )
                )
                log.info(
                    f'KeycloakMiddleware._user_is_staff - {user} - '
                    f'is_staff_roles: {is_staff_roles}'
                )
                user_roles = set(roles)
                log.info(
                    f'KeycloakMiddleware._user_is_staff - {user} - '
                    f'user_roles: {user_roles}'
                )
                is_staff = bool(is_staff_roles.intersection(user_roles))
                log.info(
                    f'KeycloakMiddleware._user_is_staff - {user} - '
                    f'is_staff: {is_staff}'
                )
                # don't write unnecessarily, check different first
                if is_staff != user.is_staff:
                    user.is_staff = is_staff
                    user.save()
        except Exception as e:
            log.warn(
                f'KeycloakMiddleware._user_is_staff - exception: {e}'
            )

    def _get_or_create_groups(self, roles: List[str]) -> List[Group]:
        groups = []
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                log.info(
                    'KeycloakMiddleware._get_or_create_groups - created: '
                    f'{group.name}'
                )
            else:
                log.info(
                    'KeycloakMiddleware._get_or_create_groups - exists: '
                    f'{group.name}'
                )
            groups.append(group)
        return groups

    def _refresh_user_groups(self, request, groups: List[Group]) -> None:
        try:
            # request.user.groups.clear()
            log.info(
                'KeycloakMiddleware._refresh_user_groups: '
                f'{[x.name for x in groups]}'
            )
            request.user.groups.set(groups)  # clears no longer existing groups
        except Exception as e:
            log.warn(
                f'KeycloakMiddleware._refresh_user_groups - exception: {e}'
            )
