# ComplyCube Python Library

The official python library for integrating with the ComplyCube API.

Check out the [API integration docs](https://docs.complycube.com/api-reference/integration).

Check out the [API reference](https://docs.complycube.com/api-reference/).


## Installation

```sh
pip install complycube
```

### Requirements

-   Python 3.6+

## Getting Started

import the client

```python
from complycube import ComplyCubeClient
```

Initialise the ComplyCubeClient with the api key from your [developer dashboard.](https://portal.doccheck.com/developers)

```python
cc_api = ComplyCubeClient(api_key='test_....')
```
Create a new client and complete a standard check

```python
input_client_dict = {
    'type':'person',
    'email':'a@b.com',
    'personDetails': {
        'firstName':'John',
        'lastName':'Smith'
    }
}
cc_client = cc_api.clients.create(**input_client_dict)
check = cc_api.checks.create(cc_client.id,'standard_screening_check')
print(check)
```

Search for clients with the first name "John"
```python
for client in ccapi.clients.list(personDetails={'firstName','John'}):
    print(client.email)
```

The auto_list function will handle api paging automatically via a generator and return a native object.
```python
for client in ccapi.clients.list(personDetails={'firstName','John'}):
    print(client.email)
```

### Per-request Configuration

As we use the requests library you can set per request configuration by using key/value pairs of any available requests parameter.

Setting the timeout for client creation to 5 seconds

```python
ccapi.clients.create(**input_client_dict, timeout=5)
```

Avoiding certification verification

```python
ccapi.clients.create(**input_client_dict, verify=False)
```

We also support the following per request settings;

Passing a specific api key for a single request

```python
ccapi.clients.create(**input_client_dict, api_key='test_...')
```

Setting number of retries to attempt

```python
ccapi.clients.create(**input_client_dict, retries=5)
```

### Configuring a Proxy

A proxy can be configured by passing in proxy object to the request:

```python
proxies = {
  'https': 'http://10.10.1.10:1080',
}
ccapi.clients.create(**input_client_dict proxies=proxies)
```

For additional information, news and our latest blogs visit us at https://www.complycube.com/