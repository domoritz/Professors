from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import BeforeRender

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""

	instance = settings.get('popit.instance', '')
	settings['popit.instance'] = instance

	config = Configurator(settings=settings)
	config.add_static_view(name = settings["static_assets"], path = 'profs:static', cache_max_age=3600)

	global profs_settings
	profs_settings = settings

	config.add_route('home', '/')
	config.add_route('search', '/search')
	config.add_route('find', '/find/{query}')
	config.add_route('details', '/details/{slug}')
	
	config.scan()
	return config.make_wsgi_app()


@subscriber(BeforeRender)
def add_global(event):
	event['tmpl_context'] = event