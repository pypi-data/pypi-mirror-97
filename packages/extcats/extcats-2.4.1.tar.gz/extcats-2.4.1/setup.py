# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extcats']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.2,<5.0', 'healpy>=1.14.0,<2.0.0', 'pymongo>=3.7,<4.0']

extras_require = \
{'ingest': ['pandas>=1.2,<2.0', 'tqdm>=4.58.0,<5.0.0']}

setup_kwargs = {
    'name': 'extcats',
    'version': '2.4.1',
    'description': 'Tools to organize and query astronomical catalogs',
    'long_description': "*******\nextcats\n*******\n\n.. image:: https://coveralls.io/repos/github/AmpelProject/extcats/badge.svg?branch=master\n   :target: https://coveralls.io/github/AmpelProject/extcats?branch=master\n\ntools to organize and query astronomical catalogs\n#################################################\n\n\nThis modules provides classes to import astronomical catalogs into \na **mongodb** database, and to efficiently query this database for \npositional matches.\n\n\nDescription:\n############\n\nThe two main classes of this module are:\n\n    - **CatalogPusher**: will process the raw files with the catalog sources and creates a database. See *insert_example* notebook for more details and usage instruction.\n    \n    - **CatalogQuery**: will perform queries on the catalogs. See *query_example* for examples and benchmarking.\n\nSupported queries includes:\n\n - all the sources with a certain distance.\n - closest source at a given position.\n - binary search: return yes/no if anything is around the positon.\n - user defined queries.\n\nThe first item on the above list (cone search around target) provides the basic block for the other two types of positional-based queries. The code supports tree types of basic\ncone-search queries, depending on the indexing strategy of the database.\n\n    - using **HEALPix**: if the catalog sources have been assigned an HEALPix index (using `healpy <https://healpy.readthedocs.io/en/latest/#>`_).\n     \n    - using **GeoJSON** (or 'legacy coordinates'): if the catalog documents have the \n      position arranged in one of these two formats (`example \n      <https://docs.mongodb.com/manual/geospatial-queries/>`_), the query is based on\n      the ``$geoWithin`` and ``$centerSphere`` mongo operators.\n    \n    - **raw**: this method uses the ``$where`` keyword to evaluate on each document a ``javascript``\n      function computing the angular distance between each source and the target. This method \n      does not require any additional field to be added to the catalog but has, in general, \n      poorer performances with respect to the methods above.\n      \nAll the core functions are defined in the ``catquery_utils`` module. In all cases the \nresults of the queries will be return an ``astropy.table.Table`` objects.\n\n\nNotes on indexing and query performances:\n-----------------------------------------\n\nThe recommended method to index and query catalogs is based on the GeoJSON coorinate type.\nSee the *example_insert* notebook for how this can be implemented. \n\n\nPerformant queries requires the database indexes to reside in the RAM. The indexes are \nefficiently compressed by mongodb default engine (WiredTiger), however there is little\nredundant (and hence compressible) information in accurately measured coordinate pairs.\nAs a consequence, GeoJSON type indexes tends to require fair amount of free memory (of \nthe order 40 MB for 2M entries). For large catalogs (and / or small RAM) indexing on \ncoordinates might not be feasible. In this case, the HEALPix based indexing should \nbe used. As (possibly) many sources shares the same HEALPix index, compression is \nmore efficient into moderating RAM usage.\n\nInstallation:\n^^^^^^^^^^^^^\n\nThe easiest way to install the Python library is with pip:\n::\n    \n    pip install extcats\n\nIf you want do modify `extcats` itself, you'll need an editable installation.\nAfter cloning this Git repository:\n::\n   \n    poetry install\n\nUsefull links:\n--------------\n\n - `mongodb installation <https://docs.mongodb.com/manual/administration/install-community/>`_\n - `healpy <https://healpy.readthedocs.io/en/latest/#>`_\n - `astropy <http://www.astropy.org/>`_\n",
    'author': 'Matteo Giomi',
    'author_email': 'matteo.giomi@desy.de',
    'maintainer': 'Jakob van Santen',
    'maintainer_email': 'jakob.van.santen@desy.de',
    'url': 'https://github.com/AmpelProject/extcats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
