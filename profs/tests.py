import unittest

from oktest import ok, test, DIFF

from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.testing import DummyResource
from pyramid.compat import url_quote, url_unquote

# uses oktest http://www.kuwata-lab.com/oktest/oktest-py_users-guide.html

# import for testing
from views import *

DIFF = repr

class UnitTests(unittest.TestCase):
	@test("query parser parses popit id")
	def _(self):
		qp = QueryParser()
		parsed = qp.parse('id:23h4jk345')
		ok(parsed) == {'id':['23h4jk345']}

	@test("query parser parses multiple popit ids")
	def _(self):
		qp = QueryParser()
		parsed = qp.parse('id:23h4jk345 id:hsdfsdfwe34')
		ok(parsed) == {'id':['23h4jk345', 'hsdfsdfwe34']}


class ViewTests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	@test("home view")
	def _(self):
		from .views import home_view
		request = DummyRequest()
		response = home_view(request)
		ok(response['error']) == None

	@test("results view")
	def _(self):
		from .views import results_view
		request = DummyRequest()
		q = 'foo bar'
		request.matchdict = {'query': q}
		response = results_view(request)

		ok(response['error']) == None
		ok(response['query']) == q


class FunctionalTests(unittest.TestCase):
	def setUp(self):
		from . import main

		app = main(None, static_assets = "static")
		from webtest import TestApp

		self.testapp = TestApp(app)

	@test("not existing page returns 404")
	def _(self):
		res = self.testapp.get('/SomePage', status=404)
		ok('Not Found').in_(res.body)

	@test("home page returns 200")
	def _(self):
		res = self.testapp.get('/', status=200)
		ok('id="home"').in_(res.body)

	@test("search page gets redirected")
	def _(self):
		q = 'foo bar'
		res = self.testapp.post('/search?query=foo bar', status=302)
		ok(res.location) == 'http://localhost/find/'+url_quote(q)

	@test("results page returns 200")
	def _(self):
		res = self.testapp.get('/find/abc', status=200)
		ok('id="results"').in_(res.body)