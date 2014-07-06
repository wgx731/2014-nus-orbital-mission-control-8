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
        self.normal_user_logout_url = {
            'url': 'https://www.google.com/accounts/Logout?continue=http%3A//testbed.example.com/',
            'url_linktext': 'Logout'
        }
        self.admin_user_logout_url = {
            'url': 'https://www.google.com/accounts/Logout?continue=http%3A//testbed.example.com/',
            'url_linktext': 'Logout'
        }

    def tearDown(self):
        self.testbed.deactivate()

    def set_current_user(self, email, user_id, is_admin=False):
        email_to_set = email or ''
        id_to_set = user_id or ''
        admin_to_set = '1' if is_admin else '0'
        self.testbed.setup_env(USER_EMAIL=email_to_set, overwrite=True)
        self.testbed.setup_env(USER_ID=id_to_set, overwrite=True)
        self.testbed.setup_env(USER_IS_ADMIN=admin_to_set, overwrite=True)

    def test_no_login_user(self):
        self.set_current_user(None, None)
        result = get_user_url('/')
        assert_that(result, equal_to(self.user_login_url))
        assert_that(result['url_linktext'], is_not('Logout'))

    def test_normal_login_user(self):
        self.set_current_user('test@test.com', 'test')
        result = get_user_url('/')
        assert_that(result, equal_to(self.normal_user_logout_url))
        assert_that(result['url_linktext'], is_not('Login'))

    def test_admin_login_user(self):
        self.set_current_user('admin@test.com', 'admin', True)
        result = get_user_url('/')
        assert_that(result, equal_to(self.admin_user_logout_url))
        assert_that(result['url_linktext'], is_not('Login'))

if __name__ == '__main__':
    unittest.main()
