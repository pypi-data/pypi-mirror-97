from ftw.protectinactive.registry import IProtectInactiveSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def migrate_to_1001(portal):
    registry = getUtility(IRegistry)
    registry.registerInterface(IProtectInactiveSettings)
