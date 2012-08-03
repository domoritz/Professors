# -*- coding: utf-8 -*-

import unittest

from oktest import ok, test, DIFF

from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.testing import DummyResource
from pyramid.compat import url_quote, url_unquote

# uses oktest http://www.kuwata-lab.com/oktest/oktest-py_users-guide.html

# import for testing
from views import *

from .views import home_view
from .views import results_view
from .views import details_view

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

	@test("parse words")
	def _(self):
		qp = QueryParser()
		parsed = qp.parse('foo bar baz')
		ok(parsed) == {'word':['foo', 'bar', 'baz']}


class ViewTests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		self.request = DummyRequest()

	def tearDown(self):
		testing.tearDown()

	@test("home view should return context dictionary")
	def _(self):
		response = home_view(self.request)
		ok(response['error']) == None

	@test("results view should return context dictionary")
	def _(self):
		q = 'foo bar'
		self.request.matchdict = {'query': q}
		response = results_view(self.request)

		ok(response['error']) == None
		ok(response['query']) == q
		ok(response['results']) == {} # no results

	@test("results view should show all results on search for all")
	def _(self):
		q = 'all'
		self.request.matchdict = {'query': q}
		response = results_view(self.request)

		ok(response['results']) == [{'name': 'Albert'}, {'name': 'Erwin'}]

	@test("results view should show results for search for id")
	def _(self):
		q = 'id:albert-einstein'
		self.request.matchdict = {'query': q}
		response = results_view(self.request)

		ok(response['results']) == [{'name': 'Albert'}]

	@test("results view should return error for non existing id")
	def _(self):
		q = 'id:non-existing-slug'
		self.request.matchdict = {'query': q}
		response = results_view(self.request)

		ok(response['error']).is_a(Exception)
		ok(response['results']) == []

	@test("details view should return context dictionary")
	def _(self):
		slug = 'albert-einstein'
		self.request.matchdict = {'slug': slug}
		response = details_view(self.request)

		ok(response['error']) == None
		ok(response['item']) == {'name': 'Albert'}

	@test("wrong slug for details should return error")
	def _(self):
		slug = 'non existing slug'
		self.request.matchdict = {'slug': slug}
		response = details_view(self.request)

		ok(response['error']).is_a(Exception)
		ok(response['item']).is_a(dict).length(0)


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


class Get():
	def __init__(self, d):
		self.d = d

	def get(self):
		return self.d

class Person():
	def __call__(self, *args, **kwargs):
		if len(args) and args[0] == 'albert-einstein':
			return Get({'result': {'name': 'Albert'}})
		raise Exception()

	def get(self):
		return {'results': [{'name': 'Albert'}, {'name': 'Erwin'}]}

class PopitMock():
	"""a mock object so that we can test the behaviour of 
	this app instead of popit itself"""

	def __getattr__(self, key):
		return Person()

	def __nonzero__(self):
		return True