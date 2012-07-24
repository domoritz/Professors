from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
	return {'project':'Professors'}

@view_config(route_name='find', renderer='templates/find.pt')
def find_view(request):

	query_string = request.params['query']
	query = query_string

	return {'project':'Professors', 'query': query}