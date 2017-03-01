thegamecrafter-python
===============

[![Build Status](https://travis-ci.org/sparr/thegamecrafter-python.svg?branch=master)](https://travis-ci.org/sparr/thegamecrafter-python)
[![Coverage Status](https://coveralls.io/repos/sparr/thegamecrafter-python/badge.svg?branch=master&service=github)](https://coveralls.io/github/sparr/thegamecrafter-python?branch=master)

A Python abstraction layer around the TheGameCrafter API.

#####Installing:

To install the thegamecrafter package simply run:

```shell
> pip install thegamecrafter
```

or include a line for 'thegamecrafter' in your projects requirements.txt and run:
```shell
> pip install -r requirements.txt
```

#####Getting Started:

The first step in using the thegamecrafter package is creating a new instance of the TheGameCrafter class by passing it your username, password, and API url. You can sign up for an account at https://thegamecrafter.com. This package's default API host is 'www.thegamecrafter.com'.

```python
from thegamecrafter import *
TGC = TheGameCrafter(username="Meeple", password="SecrEt123", apikey="1234-FAKE")
```

Once you have instantiated your TheGameCrafter class you can start to make calls to the TheGameCrafter API. You can get a list of games on your account by running the following command:

```python
gamelist = TGC.user.fetch('ABCD-1234').games
```

#####Methods:

Most exposed api endpoints support the methods `create`, `fetch`, `update`, `delete`.

Endpoints with plural names such as `announcements`, `users`, etc have the method `list`

Many endpoints have the method `_options` which enumerates the valid values for some fields.

Other unique endpoint methods, and the valid parameters that you can pass to each method, are documented at https://www.thegamecrafter.com/developer/ in the 'APIs' section.

#####Responses:

Every call to the API returns an object with some standard attributes:

```python
response.content # the JSON object from the body of the response
response.response # the python requests library response object
response.thegamecrafter # the api wrapper object used to create the call
```

Successful calls will also return the data from `content` as attributes of the object:

```python
response.id
response.name
response.visible
response.items
# etc
```

If the response is part of a paginated list then `paging` will contain some information about the page, and a method is provided to retrieve the entire list:

```python
response.paging['items_per_page']
response.paging['next_page_number']
response.paging['page_number']
response.paging['previous_page_number']
response.paging['total_items']
response.paging['total_pages']
response.items # the items from this page
response.all() # the items from every page. Watch out for timeouts and throttling.
```

Unsuccessful requests have `content` containing a single error object:

```python
response.error['code'] # the numeric error code, 4XX
response.error['message'] # a human readable explanation of the error
response.error['data'] # optional, some data specific to the error
```

Also, for unsuccessful requests a `thegamecrafter.ResponseError` can be raised if desired.  You can control this behavior by passing `raise_on_errors=True` when creating your client:

```python
from thegamecrafter import TheGameCrafter
client = TheGameCrafter(raise_on_errors=True)
client.user.fetch("nonexistent")
# raises thegamecrafter.ResponseError
```

By default, this behavior is disabled.

##### Request timeouts:

By default, this library does not enforce a time limit on requests.  A timeout may be configured by passing a `timeout` argument to the client. `timeout` may contain ([as with the underlying `requests` library][requests-timeouts]) either a single float or a tuple in the format `(connect_timeout, read_timeout)`. If a timeout occurs (either a read or connect timeout), a `thegamecrafter.TimeoutError` will be raised. Example:

```python
from thegamecrafter import TheGameCrafter, TimeoutError.
client = TheGameCrafter(timeout=(1.0, 10.0))

try:
    client.user.fetch("Meeple")
except thegamecrafter.TimeoutError:
    # retry later
```

By default, this behavior is disabled.

[requests-timeouts]: http://docs.python-requests.org/en/master/user/advanced/#timeouts

Please feel free to fork this repository at https://github.com/sparr/thegamecrafter-python and I'll be happy to incorporate modifications through pull requests.
