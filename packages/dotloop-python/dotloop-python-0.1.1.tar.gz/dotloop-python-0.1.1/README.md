# dotloop-python
Python wrapper around the dotloop API.

## Quick Start
### Authenticate
Start by getting access and refresh tokens.

```python
from dotloop import Authenticate

auth = Authenticate('dotloop-client-id', 'dotloop-client-secret')
url = auth.url_for_authentication('https://example.com/redirect/')

...
# code is received
with auth:
    response = auth.acquire_access_and_refresh_tokens(code, 'https://example.com/redirect/')
    # response is a dictionary:
    # {
    #   "access_token": "...",
    #   "token_type": "Bearer",
    #   "refresh_token": "...",
    #   "expires_in": ...,
    #   "scope": "..."
    # }
```

### Client
Then use the access token acquired to create a `Client` object.

```python
access_token = response['access_token']
client = Client(access_token)
```

From the `Client` object, you can now access dotloop data.

For example, get data about all profiles
```python
client.profile.get()  # -> Dict
```

or get data about a specific profile
```python
client.profile(<profile_id>).get()
```

or get all loops associated with a profile
```python
client.profile(<profile_id>).loop.get()
```

or get all folders in a specific loop
```python
client.profile(<profile_id>).loop(<loop_id>).folder.get()
```

or update a participant on a specific loop
```python
client.profile(<profile_id>).loop(<loop_id>).participant(<participant_id>).patch(email='newemail@example.com')
```

## Design Philosophy
All items accessible in the dotloop API follow a hierarchical structure (i.e. profiles have loops which have folders which have documents) as represented like this:

- Account
- Contact
- LoopIt
- Profile
    - LoopTemplate
    - Loop
        - Activity
        - Participant
        - Detail
        - TaskList
            - Task
        - Folder
            - Document

The design of this wrapper was intended to emulate that while providing idiomatic ways of quickly accessing data. Endpoints and their HTTP methods are easily translated to python code. 

Accessing 

    PATCH /profile/1/loop/1/folder/1

with data

    {
      "name": "Disclosures (renamed)"
    }

translates seamlessly to

```python
client.profile(1).loop(1).folder(1).patch(name='Disclosures (renamed)')
```

Note: if data keys ever have spaces then those keys can be included by unpacking a dictionary
e.g.
```python
client.profile(1).loop(1).detail.patch(**{'Property Information': {...}})
```

Inspiration was taken from [dotloop-ruby](https://github.com/sampatbadhe/dotloop-ruby) and [sendgrid-python](https://github.com/sendgrid/sendgrid-python).

## Links
[dotloop API documentation](https://dotloop.github.io/public-api/)

## To-Do
- Account
  - [x] .get
- Activity
  - [x] .get
- Contact
  - [x] .delete
  - [x] .get
  - [x] .patch
  - [x] .post
- Detail
  - [x] .get
  - [x] .patch
- Document
  - [x] .get
  - [ ] .post
- Folder
  - [x] .get
  - [x] .patch
  - [x] .post
- Loop
  - [x] .get
  - [x] .patch
  - [x] .post
- LoopIt
  - [x] .post
- LoopTemplate
  - [x] .get
- Participant
  - [x] .delete
  - [x] .get
  - [x] .patch
  - [x] .post
- Profile
  - [x] .get
  - [x] .patch
  - [x] .post
- Task
  - [x] .get
- TaskList
  - [x] .get

- Better typing
- Better passing of parameters
- Async
- Better handling of request sessions
- Better exception handling
- Better documentation
- Unit tests

```python
import asyncio

import aiohttp
import dotloop


async def main():
  async with aiohttp.ClientSession() as s:
    async with s.post()


if __name__ == '__main__':
  main()
```

## Disclaimer
I do not work for dotloop nor for Zillow.