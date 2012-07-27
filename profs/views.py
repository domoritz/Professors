from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from libs.popit.popit import PopIt, ConnectionError
import re
import logging
from pprint import pprint as pp

log = logging.getLogger(__name__)


try:
	api = PopIt(instance = 'professors', hostname = '127-0-0-1.org.uk', port = 3000, user = 'test@test.co.uk', password = 'tJo1zBum')
except ConnectionError, e:
	log.error("Cannot connect to PopIt. \n%s",str(e))

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
	return {'error': None}


@view_config(route_name='search', request_method='POST')
def search_view(request):
	query = request.params['query']
	url = request.route_url('find', query=query)

	return HTTPFound(location=url)


@view_config(route_name='find', renderer='templates/find.pt')
def results_view(request):
	query = request.matchdict['query']
	results = {}
	error = None

	qp = QueryParser()
	parsed = qp.parse(query)
	
	try:
		if parsed.has_key('id'):
			id = parsed['id'][0]
			results = [api.person(id).get()['result']]

		if parsed.has_key('word') and 'all' in parsed['word']:
			results = api.person.get()['results']

	except Exception, e:
		log.warn(e)
		raise e
		error = e

	return {'query': query, 'results': results, 'error': error}


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