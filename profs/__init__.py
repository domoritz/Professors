from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import BeforeRender

import logging
from libs.popit.popit import PopIt, ConnectionError

api = PopIt(lazy = True) # lazy initalization
def get_api():
	return api

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.add_static_view(name = settings["static_assets"], path = 'profs:static', cache_max_age=3600)

	connect_to_popit(settings)

	config.add_route('home', '/')
	config.add_route('search', '/search')
	config.add_route('find', '/find/{query}')
	config.add_route('details', '/details/{slug}')

	config.scan()
	return config.make_wsgi_app()


@subscriber(BeforeRender)
def add_global(event):
	event['tmpl_context'] = event


def connect_to_popit(settings):
	if not settings.has_key('popit.instance'):
		from tests import PopitMock
		global api
		api = PopitMock()
	else:
		try:
			api.set_up(instance = settings['popit.instance'], \
				hostname = settings['popit.hostname'], \
				port = settings['popit.port'], \
				user = settings['popit.user'], \
				password = settings['popit.password'])
		except ConnectionError, e:
			log = logging.getLogger(__name__)
			log.error("Cannot connect to PopIt. \n%s",str(e))