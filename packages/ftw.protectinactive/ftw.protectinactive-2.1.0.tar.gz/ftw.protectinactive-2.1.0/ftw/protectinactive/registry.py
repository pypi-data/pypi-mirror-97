from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope import schema


_ = MessageFactory('plone')


class IProtectInactiveSettings(Interface):
    exception_type = schema.Choice(
        title=_(u"exception_type", default=u"Exception Type"),
        description=_(
            u"exception_type_description",
            default=u"The exception raised when a user tries to access "
                    u"inactive content without permission."),
        values=['Unauthorized', 'NotFound'],
        default='Unauthorized'
    )

    is_active = schema.Bool(
        title=_(u"is_active", default=u"Globally enable/disable hook"),
        default=True,
        required=False,
        missing_value=True,
    )
