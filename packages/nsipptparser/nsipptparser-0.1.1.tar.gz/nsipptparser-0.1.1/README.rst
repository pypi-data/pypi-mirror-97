nsipptparser
============

.. image:: https://img.shields.io/pypi/v/nsipptparser.svg
    :target: https://pypi.python.org/pypi/nsipptparser
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/kragniz/cookiecutter-pypackage-minimal.png
   :target: https://travis-ci.org/kragniz/cookiecutter-pypackage-minimal
   :alt: Latest Travis CI build status

Very simple package for parsing .nsippt files to json. Use Python 3.4 and up.

Usage
-----
.. code-block:: python

    pygments_style = 'sphinx'
    import nsipptparser
    import json
    
    with open("sneaky.nsippt") as file:
        data = nsipptparser.parse(file)
        # Get the first length measurement of the first View
        length = data["ViewPropertiesSet"]["View Properties"][0]["Actions Set"]["Length"][0]["length value"]
        print("The length is ", length)
        
        # Get the base64 thumbnail of the first View
        thumbnail = data["ViewPropertiesSet"]["View Properties"][0]["Thumbnail"]
        print("The thumbnail is ", thumbnail)
        
        # Save to json file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

Note: All values are parsed as strings, so you will have to parse the strings further yourself.
            
Installation
------------
.. code-block:: shell

    pip install nsipptparser

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------
MIT

Authors
-------

`nsipptparser` was written by `Russell Tran <tranrl@stanford.edu>`_.
