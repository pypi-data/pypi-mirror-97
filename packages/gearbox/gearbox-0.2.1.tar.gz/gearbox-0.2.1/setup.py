from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

version = "0.2.1"

setup(name='gearbox',
      version=version,
      description="Command line toolkit born as a PasteScript replacement for the TurboGears2 web framework",
      long_description=README,
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Framework :: TurboGears',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='web framework command-line setup',
      author='Alessandro Molina',
      author_email='amol@turbogears.org',
      url='https://github.com/TurboGears/gearbox',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "Tempita",
        "PasteDeploy",
        "hupper >= 1.3"
      ],
      entry_points={
        'console_scripts': [
            'gearbox = gearbox.main:main'
            ],
        'gearbox.commands': [
            'makepackage = gearbox.commands.basic_package:MakePackageCommand',
            'serve = gearbox.commands.serve:ServeCommand',
            'setup-app = gearbox.commands.setup_app:SetupAppCommand',
            'scaffold = gearbox.commands.scaffold:ScaffoldCommand',
            'patch = gearbox.commands.patch:PatchCommand'
            ],
        'paste.server_runner': [
            'wsgiref = gearbox.commands.serve:wsgiref_server_runner',
            'cherrypy = gearbox.commands.serve:cherrypy_server_runner',
            ],
        'paste.server_factory': [
            'gevent = gearbox.commands.serve:gevent_server_factory',
        ]
      })
