import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all in the
# same entity group.
# Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """
    Constructs a Datastore key for a Guestbook entity with guestbook_name.
    """
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """
    Models an individual Guestbook entry with author, content, and date.

    You can create a Greeting:
    >>> greeting = Greeting(parent=guestbook_key(), content='test content')
    >>> greeting
    Greeting(key=Key('Guestbook', 'default_guestbook', 'Greeting', None), content='test content')
    >>> created_key = greeting.put()

    You can query to select the greeting:
    >>> greetings_query = Greeting.query(ancestor=guestbook_key())
    >>> list(greetings_query.fetch(10)) # doctest: +ELLIPSIS
    [Greeting(key=Key('Guestbook', 'default_guestbook', ...)]

    To modify a greeting, change one of its properties and ``put()`` it again.
    >>> greeting_2 = _[0]
    >>> greeting_2.content = 'test 2'
    >>> created_key_2 = greeting_2.put()
    >>> greeting_2.content
    u'test 2'

    Verify that the key for the greeting doesn't change.
    >>> bool(created_key == created_key_2)
    True
    """
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)
