# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.events import subscriber, BeforeRender, NewRequest
from pyramid.httpexceptions import HTTPFound, HTTPServerError
from pyramid import request

import logging
import re
from libs.popit.popit import PopIt, ConnectionError

public_api_port = 0
api = PopIt(lazy = True) # lazy initialization
def get_api():
	return api

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.add_static_view(name = settings["static_assets"], path = 'profs:static', cache_max_age=3600)

	global public_api_port
	if settings.has_key('popit.public_port'):
		public_api_port = settings['popit.public_port']
	elif settings.has_key('popit.port'):
		public_api_port = settings['popit.port']

	connect_to_popit(settings)

	config.add_route('home', '/')
	config.add_route('search', '/search')
	config.add_route('find', '/find/{query}')
	config.add_route('searchall', '/search')
	config.add_route('details', '/details/{slug}')
	config.add_route('api', '/api')
	config.add_route('explore', '/explore')

	config.scan()
	return config.make_wsgi_app()


@subscriber(BeforeRender)
def add_global(event):
	event['error'] = None
	event['tmpl_context'] = event
	if api.initialized:
		event['popit_api_url'] = re.sub('[0-9]{2,4}(?=/)', str(public_api_port) ,str(api))
	else:
		event['popit_api_url'] = "/"

def cache_callback(request, response):
    """Set the cache_control max_age for the response"""
    response.cache_control.max_age = 360

@subscriber(NewRequest)
def add_callbacks(event):
    request = event.request
    request.add_response_callback(cache_callback)


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
			log.error("Cannot connect to PopIt. Make sure Popit is running and the try again. \n%s",str(e))
			raise e