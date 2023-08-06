# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idpmodem', 'idpmodem.codecs']

package_data = \
{'': ['*']}

install_requires = \
['aioserial>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'idpmodem',
    'version': '1.3.0',
    'description': 'A library for interfacing with an Inmarsat IsatData Pro satellite modem using serial AT commands.',
    'long_description': '========\nidpmodem\n========\n\nPython library and samples for integrating with satellite Internet-of-Things \nmodems using the `Inmarsat <https://www.inmarsat.com>`_\nIsatData Pro ("IDP") network.\n\n`Documentation <https://inmarsat.github.io/idpmodem/>`_\n\nOverview\n--------\n\nIDP is a store-and-forward satellite messaging technology with\nmessages up to 6400 bytes mobile-originated or 10000 bytes mobile-terminated.\n*Messages* are sent from or to a *Mobile* using its globally unique ID,\ntransacted through a *Mailbox* that provides authentication, encryption and\ndata segregation for cloud-based or enterprise client applications via a\nnetwork **Messaging API**.\n\nThe first byte of the message is referred to as the\n*Service Identification Number* (**SIN**) where values below 16 are reserved\nfor system use.  SIN is intended to capture the concept of embedded\nmicroservices used by an application.\n\nThe second byte of the message can optionally be defined as the\n*Message Identifier Number* (**MIN**) intended to support remote operations \nwithin each embedded microservice with defined binary formatting.\nThe MIN concept also supports the optional *Message Definition File* feature\nallowing an XML file to be applied which presents a JSON-tagged message\nstructure on the network API.\n\nTerminology:\n\n* MO = **Mobile Originated** aka *Return* aka *From-Mobile*\n  message sent from modem to cloud/enterprise application\n* MT = **Mobile Terminated** aka *Forward message* aka *To-Mobile*\n  message sent from cloud/enterprise application to modem\n\nModem operation\n---------------\n\nUpon power-up or reset, the modem first acquires its location using \nGlobal Navigation Satellite Systems (GNSS).\nAfter getting its location, the modem tunes to the correct frequency, then\nregisters on the Inmarsat network.  Once registered it can communicate on the\nnetwork.\nProlonged obstruction of satellite signal will put the modem into a "blockage"\nstate from which it will automatically try to recover based on an algorithm\ninfluenced by its *power mode* setting.',
    'author': 'G.Bruce-Payne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Inmarsat/idpmodem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
