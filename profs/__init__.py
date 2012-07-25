from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view(name = settings["static_assets"], path = 'profs:static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('search', '/search')
    config.add_route('find', '/find/{query}')
    
    config.scan()
    return config.make_wsgi_app()
