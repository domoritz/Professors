# -*- coding: utf-8 -*-

from pyramid.view import view_config, notfound_view_config
from pyramid.httpexceptions import HTTPFound, HTTPServerError, exception_response
from requests.exceptions import ConnectionError, HTTPError

import re
import logging
import datetime
from pprint import pprint as pp
from profs import get_api
from libs.popit.popit import HttpClientError

log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='templates/home.pt', http_cache=datetime.timedelta(hours=1))
def home_view(request):
	return dict(error = None)

@view_config(route_name='api', renderer='templates/api.pt')
def api_view(request):
	url = get_api().get_url()
	version = get_api().get_api_version()
	online = get_api().is_online()
	return dict(error = None, version = version, url = url, online = online)

@view_config(route_name='explore', renderer='templates/explore.pt')
def explore_view(request):
	return dict(error = None)


@view_config(route_name='search', request_method='POST')
def search_view(request):
	query = request.params['query']
	url = request.route_url('find', query=query)

	return HTTPFound(location=url)


@view_config(route_name='details', renderer='templates/details.pt')
def details_view(request):
	slug = request.matchdict['slug']
	item = {}
	error = None

	if not get_api():
		return HTTPServerError(detail='Cannot connect to Popit')
	try:
		item = get_api().person(slug).get()['result']
	except Exception, e:
		log.warn(e)
		error = e

	return dict(item = item, error = error)


@view_config(route_name='find', renderer='templates/find.pt')
def results_view(request):
	query = request.matchdict['query']
	results = {}
	error = None

	qp = QueryParser()
	parsed = qp.parse(query)

	if not get_api():
		return HTTPServerError(detail='Cannot connect to Popit')
	try:
		if parsed.has_key('slug'):
			results = []
			if len(parsed['slug']) == 1:
				url = request.route_url('details', slug=parsed['slug'][0])
				return HTTPFound(location=url)
			for slug in parsed['slug']:
				results.append(get_api().person(slug).get()['result'])

		if parsed.has_key('word') and 'all' in parsed['word']:
			results = get_api().person.get()['results']

	except Exception, e:
		log.warn(e)
		error = e

	return dict(query = query, results = results, error = error)


class QueryParser(object):
	"""docstring for QueryParser"""
	def __init__(self):
		pass

	def parse(self, query):
		self.query = query
		tokens = query.split()

		parsed = {}
		for token in tokens:
			key, value = self.parse_token(token)
			if not parsed.has_key(key):
				parsed[key] = []
			parsed[key].append(value)

		return parsed

	def parse_token(self, token):
		m=re.match('(.+):(.+)', token)
		if m:
			return m.group(1), m.group(2)

		return 'word', token