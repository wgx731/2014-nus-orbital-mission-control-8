# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
from selenium.common.exceptions import NoSuchElementException
from behave import given, when, then
from hamcrest import assert_that, contains_string

HOME = "http://localhost:4567"


@given('user has been sign out')
def step_user_has_sign_out(context):
    context.browser.get(HOME)
    try:
        sign_out_link = context.browser.find_element_by_link_text('Logout')
        sign_out_link.click()
    except NoSuchElementException:
        pass


@when('I go to "{url}"')
def step_go_to(context, url):
    context.browser.get(url)


@then('I should see main page html')
def step_see_main_page(context):
    guest_name_label = 'Guestbook name:'
    page_source = context.browser.page_source
    assert_that(page_source, contains_string(guest_name_label))
    elm = context.browser.find_element_by_id("submit")
    elm.value = "Sign Guestbook"
    elm = context.browser.find_element_by_id("switch")
    elm.value = "switch"


@when('I sign "{content}"')
def setp_sign_content(context, content):
    elm = context.browser.find_element_by_name("content")
    elm.send_keys(content)
    button = context.browser.find_element_by_id("submit")
    button.click()


@then('I should see "{content}" signed by "{user}"')
def setp_see_content(context, content, user):
    page_source = context.browser.page_source
    assert_that(page_source, contains_string("<blockquote>%s</blockquote>" % content))
    assert_that(page_source, contains_string(user))
