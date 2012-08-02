from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import BeforeRender

import logging
from libs.popit.popit import PopIt, ConnectionError

#def get_api():
#	return api

class Api(object):
	def __init__(self):
		self.api = None
	def set_api(self, a):
		self.api = a
	def __call__(self):
		return self.api

api = Api()	

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.add_static_view(name = settings["static_assets"], path = 'profs:static', cache_max_age=3600)

	#global api
	api.set_api(connect_to_popit(settings))

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
		return PopitMock()

	try:
		return PopIt(instance = settings['popit.instance'], \
			hostname = settings['popit.hostname'], \
			port = settings['popit.port'], \
			user = settings['popit.user'], \
			password = settings['popit.password'])
	except ConnectionError, e:
		log = logging.getLogger(__name__)
		log.error("Cannot connect to PopIt. \n%s",str(e))