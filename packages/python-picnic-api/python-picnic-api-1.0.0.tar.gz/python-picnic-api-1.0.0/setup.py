# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_picnic_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'python-picnic-api',
    'version': '1.0.0',
    'description': '',
    'long_description': '"""""""""""""""""\nPython-Picnic-API\n"""""""""""""""""\n\n.. image:: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667\n    :target: https://www.buymeacoffee.com/MikeBrink\n    :alt: Buy me a coffee\n\nUnofficial Python wrapper for the Picnic_ API. While not all API methods have been implemented yet, you\'ll find most of what you need to build a working application are available. \n\nThis library is not affiliated with Picnic and retrieves data from the endpoints of the mobile application. Use at your own risk.\n\n.. _Picnic: https://picnic.app/nl/\n\n===============\nGetting started\n===============\nThe easiest way to install is directly from pip::\n\n    $ pip install python-picnic-api\n\n\n-----\nUsage\n-----\nI\'ll go over a few common operations here you\'ll most likely use in applications. \nTo login:\n\n.. code-block:: python\n\n    from python_picnic_api import PicnicAPI\n\n    picnic = PicnicAPI(username=\'username\', password=\'password\', country_code="NL")\n\nThe country_code parameter defaults to NL, but you have to change it if you live in a different country than the Netherlands (Germany: DE, Belgium: BE).\nYou can also store your credentials by setting the store value to true, this will store your credentials and country_code in /config/app.yaml. \n\nSearching for a product\n-----------------------\n.. code-block:: python\n\n    >>> picnic.search(\'coffee\')\n    [{\'type\': \'CATEGORY\', \'id\': \'coffee\', \'links\': [{\'type\': \'SEARCH\', \'href\': \'https://storefront-prod.nl.picnicinternational.com/api/15/search?search_term=coffee\'}], \'name\': \'coffee\', \'items\': [{\'type\': \'SINGLE_ARTICLE\', \'id\': \'10511523\', \'decorators\': [{\'type\': \'UNIT_QUANTITY\', \'unit_quantity_text\': \'500 gram\'}], \'name\': \'Lavazza espresso koffiebonen\', \'display_price\': 599, \'price\': 599, \'image_id\': \'d3fb2888fc41514bc06dfd6b52f8622cc222d017d2651501f227a537915fcc4f\', \'max_count\': 50, \'unit_quantity\': \'500 gram\', \'unit_quantity_sub\': \'€11.98/kg\', \'tags\': []}, ... \n\nCheck cart\n----------\n.. code-block:: python\n\n    >>> picnic.get_cart()\n    {\'type\': \'ORDER\', \'id\': \'shopping_cart\', \'items\': [], \'delivery_slots\': [...\n\n\nManipulating your cart\n----------------------\nAll of these methods will return the shopping cart.\n\n.. code-block:: python\n\n    # adding 2 \'Lavazza espresso koffiebonen\' to cart\n    picnic.add_product(\'10511523\', count=2)\n\n    # removing 1 \'Lavazza espresso koffiebonen\' from cart\n    picnic.remove_product(\'10511523\')\n\n    # clearing the cart\n    picnic.clear_cart()\n\nSee upcoming deliveries\n------------------------\n.. code-block:: python\n\n    >>> picnic.get_current_deliveries()\n    []\n\n\nSee available delivery slots\n----------------------------\n.. code-block:: python\n\n    >>> picnic.get_delivery_slots()\n\n',
    'author': 'Mike Brink',
    'author_email': 'mjh.brink@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MikeBrink/python-picnic-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
