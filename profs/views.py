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
from operator import sub
from itertools import imap

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

	try:
		item = get_api().person(slug).get()['result']
	except ConnectionError, e:
		log.warn(e)
		error = e
	except HttpClientError, e:
		# i.e. 404 not found error
		log.warn(e)
		if e:
			details = "The requested resource could not be found. You may want to try another slug."
			raise exception_response(404)

	return dict(item = item, error = error)


@view_config(route_name='find', renderer='templates/results.pt')
def results_view(request):
	query = request.matchdict['query']
	results = []
	error = None

	qp = QueryParser()
	parsed = qp.parse(query)

	try:
		if parsed.has_key('slug'):
			res = {'name': 'Slug', 'data': []}
			if len(parsed['slug']) == 1:
				url = request.route_url('details', slug=parsed['slug'][0])
				return HTTPFound(location=url)
			for slug in parsed['slug']:
				res['data'].append(get_api().person(slug).get()['result'])
			results.append(res);

		elif parsed.has_key('word') and 'all' in parsed['word']:
			res = {'name': 'All'}
			res['data'] = get_api().person.get()['results']
			results.append(res)
            
		elif parsed.has_key('word'):
			name = {'name': 'Name', 'data': []}
			summary = {'name': 'Summary', 'data': []}
			for q in parsed['word']:
				name['data'] += get_api().person().get(name=q)['results']
				summary['data'] += get_api().person().get(summary=q)['results']
			#summary['data'] = list(imap(sub, summary['data'], name['data']))
			results.append(name)
			results.append(summary)

	except ConnectionError, e:
		log.warn(e)
		error = "ConnectionError. The PopIt API is currently not available."
	except HTTPError, e:
		log.warn(e)
		error = e

	print results

	# remove empty items, this is faster that filter(lambda x: x, results) but does the same
	# None is the identity function according to the docs
	results = filter(None, results)

	return dict(query = query, results = results, error = error)


@notfound_view_config(renderer="templates/404.pt")
def notfound(request):
	request.response.status = 404
	return dict()


class QueryParser(object):
	"""docstring for QueryParser"""
	def __init__(self):
		pass

	def parse(self, query):
		self.query = query
		tokens = self.query.split()

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