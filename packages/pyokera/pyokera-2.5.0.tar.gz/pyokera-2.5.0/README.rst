pyokera
=========

Python client for RecordService implementations.

Dependencies
------------

Required:

-  Python 3.4+

-  ``six``, ``bit_array``, ``thriftpy2==0.3.12``, ``urllib3``, ``certifi``

.. code:: shell

    pip3 install six bit_array thriftpy2==0.3.12 urllib3 certifi

Optional:

-  ``pandas`` for conversion to ``DataFrame`` objects

Installation
------------

.. code:: shell

    pip3 install pyokera

To verify:

.. code:: python

    >>> import okera.odas
    >>> okera.odas.version()
    '##OKERA_RELEASE_VERSION##'

Usage
~~~~~

.. code:: python

    from okera import context
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        conn.list_databases()
        pd = conn.scan_as_pandas("okera_sample.sample")
        pd

To enable a connection to a server with token-authentication:

.. code:: python

    from okera import context
    ctx = context()
    ctx.enable_token_auth(token_str='my-token')
    with ctx.connect(host='localhost', port=12050) as conn:
        conn.list_databases()

To enable a connection to a server with kerberos-authentication:

.. code:: python

    from okera import context
    ctx = context()
    # Connecting to server principal 'cerebro/service@REALM'
    ctx.enable_kerberos('cerebro', host_override='service')
    with ctx.connect(host='localhost', port=12050) as conn:
        conn.list_databases()
