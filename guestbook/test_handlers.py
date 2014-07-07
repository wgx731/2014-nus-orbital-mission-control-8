import unittest

from hamcrest import assert_that, equal_to, contains_string
import webtest

from google.appengine.ext import testbed
from guestbook import make_application


class HandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()
        self.testapp = webtest.TestApp(make_application())
        self.status_ok = 200
        self.html_content_type = "text/html"
        self.login_string = 'Login'
        self.logout_string = 'Logout'
        self.submit_button = '<div><input type="submit" value="Sign Guestbook"></div>'
        self.switch_button = '<input type="submit" value="switch">'
        self.guest_name_label = 'Guestbook name:'
        self.css_link = '<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />'

    def tearDown(self):
        self.testbed.deactivate()

    def set_current_user(self, email, user_id, is_admin=False):
        email_to_set = email or ''
        id_to_set = user_id or ''
        admin_to_set = '1' if is_admin else '0'
        self.testbed.setup_env(USER_EMAIL=email_to_set, overwrite=True)
        self.testbed.setup_env(USER_ID=id_to_set, overwrite=True)
        self.testbed.setup_env(USER_IS_ADMIN=admin_to_set, overwrite=True)

    def check_html(self, response_body):
        assert_that(response_body, contains_string(self.submit_button))
        assert_that(response_body, contains_string(self.switch_button))
        assert_that(response_body, contains_string(self.guest_name_label))
        assert_that(response_body, contains_string(self.css_link))

    def test_main_page_no_login(self):
        self.set_current_user(None, None)
        response = self.testapp.get('/')
        assert_that(response.status_int, equal_to(self.status_ok))
        assert_that(response.content_type, equal_to(self.html_content_type))
        body = response.normal_body
        self.check_html(body)
        assert_that(body, contains_string(self.login_string))

    def test_main_page_with_login(self):
        self.set_current_user('test@test.com', 'test')
        response = self.testapp.get('/')
        assert_that(response.status_int, equal_to(self.status_ok))
        assert_that(response.content_type, equal_to(self.html_content_type))
        body = response.normal_body
        self.check_html(body)
        assert_that(body, contains_string(self.logout_string))

    # TODO: add test for Guestbook page
