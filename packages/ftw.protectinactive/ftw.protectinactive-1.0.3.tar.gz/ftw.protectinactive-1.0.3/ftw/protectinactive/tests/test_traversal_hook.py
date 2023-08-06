from AccessControl import Unauthorized
from DateTime.DateTime import DateTime
from datetime import datetime
from datetime import timedelta
from ftw.builder import Builder
from ftw.builder import create
from ftw.protectinactive.registry import IProtectInactiveSettings
from ftw.protectinactive.tests import FunctionalTestCase
from ftw.protectinactive.tests.dx_folder import setup_dx_folder
from ftw.testbrowser import browsing
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import transaction


class TestTraversalHook(FunctionalTestCase):

    def setUp(self):
        super(TestTraversalHook, self).setUp()
        self.grant('Manager')

        setup_dx_folder(self.portal)

        # no dates
        self.no_dates_atfolder = create(Builder('folder'))
        self.no_dates_dxfolder = create(Builder('dx folder'))

        # active
        ateffective = DateTime() - 10
        atexpiration = DateTime() + 10
        dxeffective = datetime.now() - timedelta(days=10)
        dxexpiration = datetime.now() + timedelta(days=10)
        self.active_atfolder = create(Builder('folder')
                                      .having(effectiveDate=ateffective,
                                              expirationDate=atexpiration))
        self.active_dxfolder = create(Builder('dx folder')
                                      .having(effective=dxeffective,
                                              expires=dxexpiration))

        # past content
        ateffective = DateTime() - 20
        atexpiration = DateTime() - 10
        dxeffective = datetime.now() - timedelta(days=20)
        dxexpiration = datetime.now() - timedelta(days=10)
        self.past_atfolder = create(Builder('folder')
                                    .having(effectiveDate=ateffective,
                                            expirationDate=atexpiration))
        self.past_dxfolder = create(Builder('dx folder')
                                    .having(effective=dxeffective,
                                            expires=dxexpiration))

        # future content
        ateffective = DateTime() + 10
        atexpiration = DateTime() + 20
        dxeffective = datetime.now() + timedelta(days=10)
        dxexpiration = datetime.now() + timedelta(days=20)
        self.future_atfolder = create(Builder('folder')
                                      .having(effectiveDate=ateffective,
                                              expirationDate=atexpiration))
        self.future_dxfolder = create(Builder('dx folder')
                                      .having(effective=dxeffective,
                                              expires=dxexpiration))

    @browsing
    def test_manager_can_access_everything(self, browser):
        browser.login()
        try:
            browser.open(self.no_dates_atfolder)
            browser.open(self.no_dates_dxfolder)
            browser.open(self.active_atfolder)
            browser.open(self.active_dxfolder)
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("A Manager has to be able to access all content.")

    @browsing
    def test_editor_can_access_everything(self, browser):
        editor = create(Builder('user').with_roles('Editor', on=self.portal))
        browser.login(editor.getId())

        try:
            browser.open(self.no_dates_atfolder)
            browser.open(self.no_dates_dxfolder)
            browser.open(self.active_atfolder)
            browser.open(self.active_dxfolder)
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("An Editor has to be able to access the content.")

    @browsing
    def test_normal_user_access_rights(self, browser):
        user = create(Builder('user'))
        browser.login(user.getId())

        try:
            browser.open(self.no_dates_atfolder)
            browser.open(self.no_dates_dxfolder)
            browser.open(self.active_atfolder)
            browser.open(self.active_dxfolder)
        except Unauthorized:
            self.fail("A normal user has to be able to access active content.")

        with browser.expect_unauthorized():
            browser.open(self.past_atfolder)
        with browser.expect_unauthorized():
            browser.open(self.past_dxfolder)
        with browser.expect_unauthorized():
            browser.open(self.future_atfolder)
        with browser.expect_unauthorized():
            browser.open(self.future_dxfolder)

    @browsing
    def test_user_with_inactive_rights_can_access_past_content(self, browser):
        user = create(Builder('user'))
        browser.login(user.getId())
        self.portal.manage_permission('Access inactive portal content', user.getRoles())
        transaction.commit()

        try:
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
        except Unauthorized:
            self.fail("User has inactive rights but can't access inactive content.")

        with browser.expect_unauthorized():
            browser.open(self.future_atfolder)
        with browser.expect_unauthorized():
            browser.open(self.future_dxfolder)

    @browsing
    def test_user_with_future_rights_can_access_future_content(self, browser):
        user = create(Builder('user'))
        browser.login(user.getId())
        self.portal.manage_permission('Access future portal content', user.getRoles())
        transaction.commit()

        try:
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("User has future rights but can't access future content.")

        with browser.expect_unauthorized():
            browser.open(self.past_atfolder)
        with browser.expect_unauthorized():
            browser.open(self.past_dxfolder)

    @browsing
    def test_user_can_access_active_content_within_an_inactive_container(self, browser):
        self.nested_atfolder = create(Builder('folder')
                                      .within(self.past_atfolder))
        self.nested_dxfolder = create(Builder('dx folder')
                                      .within(self.past_dxfolder))

        user = create(Builder('user'))
        browser.login(user.getId())

        try:
            browser.open(self.nested_atfolder)
            browser.open(self.nested_dxfolder)
        except Unauthorized:
            self.fail("User has to be able to access active content within "
                      "an inactive container.")

    @browsing
    def test_disable_plugin(self, browser):
        with browser.expect_unauthorized():
            browser.open(self.past_atfolder)
        with browser.expect_unauthorized():
            browser.open(self.past_dxfolder)
        with browser.expect_unauthorized():
            browser.open(self.future_atfolder)
        with browser.expect_unauthorized():
            browser.open(self.future_dxfolder)

        self._disable_hook()

        try:
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("A normal user can access the content, since the plugin is disabled")

    def _disable_hook(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IProtectInactiveSettings, check=False)
        settings.is_active = False
        transaction.commit()
