Tradologics Python SDK
======================

This is the initial version of Tradologics' Python SDK.

At the moment, it only supports a wrapper for the awesome `requests` library that will automatically:

- prepend the full endpoint url to your calls
- attach your token to the request headers
- add `datetime` to your order when in backtesting mode


Install using PyPi
------------------

.. code:: bash

    $ pip3 install -U tradologics



Using the library:
------------------

In your `requirements.txt`:

.. code:: text

    tradologics


In your code:

.. code:: python

    # import Tradologics' requests
    import tradologics.requests as requests

    # set your token (once)
    requests.set_token("MY TOKEN")

    # from this point - use is just like you would have used `reqeuests`:
    requests.post("/orders", json={
        ...
    })

