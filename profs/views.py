from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from libs.popit.popit import PopIt, ConnectionError
import re
import logging
from pprint import pprint as pp
from profs import profs_settings as settings


log = logging.getLogger(__name__)

def connect_to_popit():
	try:
		return PopIt(instance = settings['popit.instance'], \
			hostname = settings['popit.hostname'], \
			port = settings['popit.port'], \
			user = settings['popit.user'], \
			password = settings['popit.password'])
	except ConnectionError, e:
		log.error("Cannot connect to PopIt. \n%s",str(e))

api = connect_to_popit()


@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
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

	if not api:
		return {'error': 'Server error 500, Not connected to PopIt.'}

	try:
		item = api.person(slug).get()['result']
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

	if not api:
		return {'error': 'Server error 500, Not connected to PopIt.'}
	
	try:
		if parsed.has_key('id'):
			id = parsed['id'][0]
			results = [api.person(id).get()['result']]

		if parsed.has_key('word') and 'all' in parsed['word']:
			results = api.person.get()['results']

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