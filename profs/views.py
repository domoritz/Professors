from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


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

	return {'query': query}