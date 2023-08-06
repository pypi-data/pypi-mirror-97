# Benchling SDK

A Python 3.7+ SDK for the [Benchling](https://www.benchling.com/) platform designed to provide typed, fluent
interactions with [Benchling APIs](https://docs.benchling.com/reference).

*Important!* This is a pre-release alpha. Changes to this project may not be backwards compatible.

## Getting Started

### Installation

Install the dependency via [Poetry](https://python-poetry.org/) (if applicable):

```bash
poetry add benchling-sdk
```
 
Or [Pip](https://pypi.org/project/pip/):
 
```bash
pip install benchling-sdk
```

### Using the SDK

Obtain a valid API key from your Benchling account and provide it to the SDK, along with the URL for the server.
Example:

```python
from benchling_sdk.benchling import Benchling
benchling = Benchling(url="https://my.benchling.com", api_key="api_key")
```

With `Benchling` now instantiated, make a sample call to get a custom entity with the ID `"custom_id"`.

```python
entity = benchling.custom_entities.get_by_id(entity_id="custom_id")
```

API calls made by the SDK are synchronous and blocking.

### Generators and nextToken

Paginated API endpoints listing objects and supporting the `nextToken` parameter will produce a `PageIterator`, which
is a [Python generator](https://wiki.python.org/moin/Generators). Example:

```python
requests_generator = benchling.requests.list(schema_id="assaych_test")
next_request = next(requests_generator)
```

In this example, `requests_generator` is a generator. Each iteration will return a `List` of `Request`s, not an 
individual `Request`.

The `PageIterator` object has an `estimated_count()` which will return the value of the `Result-Count` header from
the API, if applicable for the endpoint. If the endpoint in question does not support the header, will raise a 
`NotImplementedError` instead.

`PageIterator` also supports `first()` which will return an optional first element in the list. Using DNA Sequences as
an example, if at least one DNA sequence was returned by the results list, `first()` will return the first DNA sequence.

`first()` operates independent of iteration, meaning calls to `first()` after starting iteration will still 
return the first item from the first page and not the current page. 

If no results were available, `first()` will return `None`.

```python
from typing import Optional
from benchling_sdk.models import DnaSequence

dna_sequences_generator = benchling.dna_sequences.list()

# Typing is optional to illustrate the expected return
first_sequence: Optional[DnaSequence] = dna_sequences_generator.first()
if first_sequence:
   print(f"The first sequence was {first_sequence.id}")
else:
   print("No sequence found")
```

### Working with Benchling Fields

Many objects in Benchling have the concept of `fields`. They are represented in the SDK via the 
`benchling_sdk.models.Fields` class.

To conveniently construct `Fields` from a dictionary, we have provided a `fields` method 
in the `serialization_helper` module:

```python
from benchling_sdk.helpers.serialization_helpers import fields
from benchling_sdk.models import CustomEntity

entity = CustomEntity(
    name="My Entity",
    fields=fields({
    "a_field": {"value": "First value"},
    "second_field": {"value": "Second value"},
    })
)
```

### Async Tasks

Many Benchling endpoints that perform expensive operations launch [Tasks](https://docs.benchling.com/reference#tasks).
These are modeled in the SDK as `benchling_sdk.models.AsyncTask`.

To simply retrieve the status of a task given its id:

```python
async_task = benchling.tasks.get_by_id("task_id")
```

This will return the `AsyncTask` object, which may still be in progress. More commonly, it may be desirable to delay
further execution until a task is completed.

In this case, you may block further processing until the task is no longer `RUNNING`:

```python
completed_task = benchling.tasks.wait_for_task("task_id")
```

The `wait_for_task` method will return the task once its status is no longer `RUNNING`. This does not guarantee
the task executed successfully (see `benchling_sdk.models.AsyncTaskStatus`), only that 
Benchling considers it complete.

`wait_for_task` can be configured by optionally specifying `interval_wait_seconds` for the time to wait between calls and 
`max_wait_seconds` which is the maximum number of seconds before `wait_for_task` will give up and raise 
`benchling_sdk.errors.WaitForTaskExpiredError`.

```python
# Check the task status once every 2 seconds for up to 60 seconds
completed_task = benchling.tasks.wait_for_task(task_id="task_id", interval_wait_seconds=2, max_wait_seconds=60)
```

### Unset

The Benchling SDK uses the type `benchling_api_client.types.Unset` and the constant value 
`benchling_api_client.types.UNSET` to represent values that were not present in an interaction with the API. This is to
distinguish from values that were explicitly set to `None` from those that were simply unspecified.

A common example might be updating only specific properties of an object:

```python
from benchling_sdk.models import CustomEntityUpdate

update = CustomEntityUpdate(name="New name")

updated_entity = benchling.custom_entities.update(
    entity_id="entity_id", entity=update
)
```

All other properties of `CustomEntityUpdate` besides `name` will default to `UNSET` and not be sent with the update. Setting any
optional property to `None` will send a `null` JSON value. In general, you should not need to set `UNSET` directly.

When receiving objects from the API, some of their fields may be `Unset`. To treat `UNSET` values equivalent to 
`Optional[T]`, you can use the convenience function `unset_as_none()`:

```python
from benchling_sdk.helpers.serialization_helpers import unset_as_none

sample_value: Union[Unset, None, int] = UNSET

optional_value = unset_as_none(sample_value)
# optional_value will be None
```

### Error Handling

Failed API interactions will generally return a `BenchlingError`, which will contain some underlying
information on the HTTP response such as the status. Example:

```python
from benchling_sdk.errors import BenchlingError

try:
    requests = benchling.requests.get_by_id("request_id")
except BenchlingError as error:
    print(error.status_code)
```

If an HTTP error code is not returned to the SDK or deserialization fails, an unbounded `Exception` 
could be raised instead.

### Advanced Use Cases

By default, the Benchling SDK is designed to be opinionated towards most common usage. There is some more 
advanced configuration available for use cases which require it.

### Retries

The SDK will automatically retry certain HTTP calls when the calls fail and certain conditions are met.

The default strategy is to retry calls failing with HTTP status codes `429`, `502`, `503`, and `504`. The rationale for
these status codes being retried is that many times they are indicative of a temporary network failure or exceeding the
rate limit and may be successful upon retry.

Retries will be attempted up to 5 times, with an exponential time delay backoff between calls.

To disable retries, specify `None` for `retry_strategy` when constructing `Benchling`:

```python
benchling = Benchling(url="https://my.benchling.com", api_key="api_key", retry_strategy=None)
```

Alternatively, instantiate your own `benchling_sdk.retry_helpers.RetryStrategy` to further customize retry behavior.

### BenchlingApiClient Customization (e.g., HTTP Timeout Settings)

While the SDK abstracts most of the HTTP transport layer, access can still be granted via the `BenchlingApiClient`. A
common use case might be extending HTTP timeouts for all calls.

This can be achieved by specifying a function which accepts a default configured instance of `BenchlingApiClient` and
returns a mutated instance with the desired changes.

For example, to set the HTTP timeout to 180 seconds:

```python
from benchling_api_client.benchling_client import BenchlingApiClient

def higher_timeout_client(client: BenchlingApiClient) -> BenchlingApiClient:
    return client.with_timeout(180)


benchling = Benchling(
    url="https://my.benchling.com",
    api_key="api_key",
    client_decorator=higher_timeout_client,
)
```

To fully customize the `BenchlingApiClient` and ignore default settings, construct your own instance in lieu of 
modifying the `client` argument.

#### Changing the Base URL

When instantiating `Benchling`, the path `/api/v2` will automatically be appended to the server information provided.

For example, if creating `Benchling` like this:

```python
benchling = Benchling(url="https://my.benchling.com", api_key="api_key")
```

API calls will be made to `https://my.benchling.com/api/v2`.

To specify, an alternative path, set the `base_path` when creating `Benchling`:

```python
benchling = Benchling(url="https://my.benchling.com", api_key="api_key", base_path="/api/custom")
```

In this case, API calls will be made to `https://my.benchling.com/api/custom`.

### Custom API Calls

For making customized API calls to Benchling, the SDK supports an open-ended `Benchling.api` namespace that exposes
varying levels of interaction for HTTP `GET`, `POST`, `PATCH`, and `DELETE` methods. This is useful for API endpoints
which the SDK may not support yet or more granular control at the HTTP layer.

For each verb, there are two related methods. Using `GET` as an example:

1. `get_response()` - Returns a `benchling_api_client.types.Response` which has been parsed to a JSON `dict` 
   and is slightly more structured.
2. `get_modeled()` - Returns any custom model which extends `benchling_sdk.helpers.serialization_helpers.DeserializableModel`
   and must be a Python `@dataclass`.

Both will automatically retry failures according to `RetryStrategy` and will marshall errors to `BenchlingError`.

When calling any of the methods in `Benchling.api`, specify the **full path** to the URL except for the scheme and server. 
This differs from other API services, which will prepend the URL with a `base_path`.

For example, if wishing to call an endpoint `https://my.benchling.com/api/v2/custom-entities?some=param`, 
pass `api/v2/custom-entities?some=param` for the `url`.

Here's an example of making a custom call with `post_modeled()`:

```python
from dataclasses import dataclass, field
from typing import Any, Dict
from dataclasses_json import config
from benchling_sdk.helpers.serialization_helpers import DeserializableModel, SerializableModel

@dataclass
class ModeledCustomEntityPost(SerializableModel):
    name: str
    fields: Dict[str, Any]
    # If the property name in the API JSON payload does not match the Python attribute, use
    # field and config to specify the appropriate name for serializing/deserializing
    folder_id: str = field(metadata=config(field_name="folderId"))
    schema_id: str = field(metadata=config(field_name="schemaId"))


@dataclass
class ModeledCustomEntityGet(DeserializableModel):
    id: str
    name: str
    fields: Dict[str, Any]
    folder_id: str = field(metadata=config(field_name="folderId"))

# Assumes `benchling` is already configured and instantiated as `Benchling`
body = ModeledCustomEntityPost(
    name="My Custom Entity Model",
    folder_id="folder_id",
    schema_id="schema_id",
    fields={"My Field": {"value": "Modeled Entity"}},
)

created_entity = benchling.api.post_modeled(
    url="api/v2/custom-entities", body=body, target_type=ModeledCustomEntityGet
)
```

The returned `created_entity` will be of type `ModeledCustomEntityGet`. Classes extending `SerializableModel` and
`DeserializableModel` will inherit `serialize()` and `deserialize()` methods respectively which will act on Python 
class attributes by default. These can be overridden for more customized serialization needs.