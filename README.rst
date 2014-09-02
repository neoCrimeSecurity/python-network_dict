================
network_dict 0.1
================

Summary
=======

network_dict creates a network subnet based dictionary that returns the most specific subnet(s) for a given IP.  It will work equally with both IPv4 and IPv6.

There's a few more simple bells and whistles to make the library useful in different circumstances.

This is a case where examples speak louder than words...

Simple Example
--------------

.. code:: python

    from network_dict import NetworkDict

    networks = {
        '0.0.0.0/0': 'Everything',
        '10.0.0.0/8': 'Office',
        '10.1.0.0/16': 'Region 1',
        '10.1.1.0/24':  'City 1'
        }

    ns = NetworkDict(networks)

    >>> nd['10.1.1.1']
    'City 1'
   
    >>> nd.firstHit = False
    # Return all matching values in a list
    # Results are in order, most to least specific
    >>> nd['10.1.1.1']
    ['City 1', 'Region 1', 'Office', 'Everything']

    >>> nd.format = "both"
    # return both the subnet and value in a tuple, default is "value"
    >>> nd['10.1.1.1']
    [('10.1.1.0/24', 'City 1'), ('10.1.0.0/16', 'Region 1'), ('10.0.0.0/8', 'Office'), ('0.0.0.0/0', 'Everything')]

    >>> nd.format = "key"
    # return just the subnet address
    >>> nd['10.1.1.1']
    ['10.1.1.0/24', '10.1.0.0/16', '10.0.0.0/8', '0.0.0.0/0']

Adding Subnets
--------------

.. code:: python

    >>>  nd['192.168.1.1']
    ['0.0.0.0/0']
    # If 0.0.0.0/0 is not set, will return KeyError exception
    >>> nd['192.168.1.1/16'] = 'Home'
    >>> nd['192.168.1.1']
    ['192.168.0.0/16', '0.0.0.0/0']
    # Note that the key was normalized to a proper subnet


Hosts (IPv4 /32 or IPv6 /128)
-----------------------------

Host records are ignored by default.  If not netmask is supplied, a hostmask is assumed.

You can optionally enable hosts.  This will likely change to smallest accepted prefix, in the future.

.. code:: python

    >>> nd['10.1.1.1'] = 'Router'
    >>> nd['10.1.1.1']
    ['10.1.1.0/24', '10.1.0.0/16', '10.0.0.0/8', '0.0.0.0/0']
    # Hosts are ignored by default
    >>> nd.ignoreHosts = False
    >>> nd['10.1.1.1'] = 'Router'
    ['10.1.1.1/32', '10.1.1.0/24', '10.1.0.0/16', '10.0.0.0/8', '0.0.0.0/0']

IPv6 Subnets
------------

.. code:: python

    >>> nd['::1']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: No matching networks found, and no default network set
    # we didn't set '::/0', which is different from the '0.0.0.0/0' subnet
    >>> nd['::1/128'] = 'Localhost'
    # Note: /128 is a hostmask, so will be ignored if ignoreHosts = True (default)
    >>> nd['::1']
    ['::1/128']

Setting options at creation
---------------------------

.. code:: python

    >>> nd = NetworkDict(format = 'both', firstHit = False, ignoreHosts = True)
    # Returns an empty NetworkDict object, but with default options set
    >>> nd['192.168.0.0/16'] = 'Home'
    >>> nd['192.168.1.1']
    [('192.168.0.0/16', 'Home')]


Requirements
============

* Tested on python 2.7
* netaddr library

Installation
============

Via pip or easy_install
-----------------------

.. code:: bash

    $ sudo pip install network_dict   # If you prefer PIP

    $ sudo easy_install network_dict  # If you prefer easy_install

Manual installation
-------------------

.. code:: bash

    $ git clone https://github.com/neoCrimeLabs/python-network_dict.git
    $ cd python-network_dict
    $ sudo python setup.py install


Conditions of Use
=================

I wrote this library for my own use, but realized others may find it useful.

Unfortunately I cannot guarentee any active support, but will do my best as time
permits.  That said, I'll happily accept push requests with suitable changes
that address the general audience of this library.

Put simply, use this at your own risk.  If it works, great!  If not, I may not
be able to help you.  If you fix anything, however, please push it back and I'll
likely accept it.  :-)

Also, if you use this library in your package, tool, or comercial software, let
me know, and I'll list it here!
