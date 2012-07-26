from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from libs.popit.popit import PopIt
import re

api = PopIt(instance = 'professors', hostname = '127-0-0-1.org.uk', port = 3000, user = 'test@test.co.uk', password = 'tJo1zBum')

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
	return {'project':'Professors'}


@view_config(route_name='search', request_method='POST')
def search_view(request):
	query = request.params['query']
	url = request.route_url('find', query=query)

	return HTTPFound(location=url)


@view_config(route_name='find', renderer='templates/find.pt')
def results_view(request):
	query = request.matchdict['query']

	qp = QueryParser()
	parsed = qp.parse(query)

	if parsed.has_key('id'):
		id = parsed['id'][0]
		results = api.person(id).get()

	return {'query': query}


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