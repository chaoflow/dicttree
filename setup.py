from setuptools import setup, find_packages
import sys, os

version = '0dev'
shortdesc = 'Tree of dictionary-like nodes'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='dicttree',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development',
          ],
      keywords='',
      author='Florian Friesdorf',
      author_email='flo@chaoflow.net',
      url='http://github.com/chaoflow/metachao',
      license='BSD license',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'metachao',
          'interlude',       # for testing
          'zope.interface',  # XXX: make this optional?
          'ordereddict'      # XXX: make this optional?
          ],
      )
