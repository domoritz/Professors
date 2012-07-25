import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'WebTest',
    'nose',
    'coverage',
    ]

setup(name='profs',
      version='0.1',
      description='A repository for data on professors.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Open Data :: Professors",
        ],
      author='Dominik Moritz',
      author_email='',
      url='',
      license='Apache 2',
      keywords='web popit professors',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="profs",
      entry_points = """\
      [paste.app_factory]
      main = profs:main
      """,
      )

