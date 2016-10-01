from setuptools import setup

setup(
    name='django-search-views',
    version='0.2.0',
    url='https://github.com/inmagik/django-search-views',
    install_requires=[
        'Django >=1.8',
    ],
    description="Search List class-based views for Django",
    long_description=open('README.rst', 'r').read(),
    license="MIT",
    author="Mauro Bianchi",
    author_email="bianchimro@gmail.com",
    packages=['searchlist_views'],
    package_dir={'searchlist_views': 'searchlist_views'},
    include_package_data = True,    # include everything in source control
    package_data={'searchlist_views': ['*.py','contrib/*.py','tests/*.py','tests/templates/*.html', 'tests/templates/extra_views/*.html']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python']
)
