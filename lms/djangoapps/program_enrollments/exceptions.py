"""
Exceptions raised by functions exposed by program_enrollments Django app.
"""
from __future__ import absolute_import, unicode_literals

# Every `__init__` here calls empty Exception() constructor.
# pylint: disable=super-init-not-called


class ProgramDoesNotExistException(Exception):

    def __init__(self, program_uuid):
        self.program_uuid = program_uuid

    def __str__(self):
        return 'Unable to find catalog program matching uuid {}'.format(self.program_uuid)


class OrganizationDoesNotExistException(Exception):
    pass


class ProgramHasNoAuthoringOrganizationException(OrganizationDoesNotExistException):

    def __init__(self, program_uuid):
        self.program_uuid = program_uuid

    def __str__(self):
        return (
            'Cannot determine authoring organization key for catalog program {}'
        ).format(self.program_uuid)


class BadOrganizationShortNameException(OrganizationDoesNotExistException):

    def __init__(self, organization_short_name):
        self.organization_short_name = organization_short_name

    def __str__(self):
        return 'Unable to find organization for short_name {}'.format(
            self.organization_short_name
        )


class ProviderDoesNotExistException(Exception):

    def __init__(self, organization):
        self.organization = organization

    def __str__(self):
        return 'Unable to find organization for short_name {}'.format(
            self.organization.id
        )


class ProviderConfigurationException(Exception):

    def __init__(self, organization):
        self.organization = organization

    def __str__(self):
        return (
            'Multiple active SAML configurations found for organization={}. '
            'Expected one.'
        ).format(self.organization.short_name)
