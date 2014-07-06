import unittest

from hamcrest import assert_that, equal_to, is_not

from google.appengine.ext import testbed
from guestbook import get_user_url


class GetUserUrlTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_user_stub()
        # Set up expected values
        self.user_login_url = {
            'url': 'https://www.google.com/accounts/Login?continue=http%3A//testbed.example.com/',
            'url_linktext': 'Login'
        }

    def tearDown(self):
        self.testbed.deactivate()

    def setCurrentUser(self, email, user_id, is_admin=False):
        email_to_set = email or ''
        id_to_set = user_id or ''
        admin_to_set = '1' if is_admin else '0'
        self.testbed.setup_env(USER_EMAIL=email_to_set, overwrite=True)
        self.testbed.setup_env(USER_ID=id_to_set, overwrite=True)
        self.testbed.setup_env(USER_IS_ADMIN=admin_to_set, overwrite=True)

    def testNoLoginUser(self):
        self.setCurrentUser(None, None)
        result = get_user_url('/')
        assert_that(result, equal_to(self.user_login_url))
        assert_that(result['url_linktext'], is_not('Logout'))

    # TODO: test login with a user
