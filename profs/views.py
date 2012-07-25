from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.compat import url_quote, url_unquote

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
	return {'project':'Professors'}

@view_config(route_name='search', request_method='POST')
def search_view(request):
	query = request.params['query']
	query_string = url_quote(query)
	url = request.route_url('find', query=query_string)

	return HTTPFound(location=url)

@view_config(route_name='find', renderer='templates/find.pt')
def results_view(request):
	query_string = request.matchdict['query']
	query = url_unquote(query_string)

	return {'project':'Professors', 'query': query}