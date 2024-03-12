# Pyscript Dot Com

This is a utility package that allows you to interact with various PyScript.com features easily and simply without the need to handle any low-level API calls.

This module is currently in Alpha phase, and there are some caveats:
- making a proxy request or using project/account datastores may block your application until the request is finished
- micropython is currently not supported
- Potential bugs from an Alpha release

## Proxies

Pyscript proxies allow you to call an endpoint created in your PyScript.com account. This is useful for calling endpoints that may require credentials or just APIs that you don't want to expose to the public.

### Setting proxies

Let's first [login to pyscript.com](https://pyscript.com/) and once logged in, go to your [settings](https://pyscript.com/settings) and select **API Proxies**. Here you can create a new proxy by clicking on the **Create a new API Proxy** button and fill in the necessary fields.

Assume that you have created a proxy with the name `cat-facts` and the endpoint `https://catfact.ninja/fact`, the method will be `GET`. You can now import `proxy` from the `pyscript_dot_com` package in your pyscript app and use it to call the endpoint with the right method:

```python
from pyscript_dot_com import proxy

response = proxy('cat-facts', 'GET')
```

If you print your response you will see something similar to:

```
{"fact":"Cats sleep 16 to 18 hours per day. When cats are asleep, they are still alert to incoming stimuli. If you poke the tail of a sleeping cat, it will respond accordingly.","length":167}
```


## Datastores

Pyscript datastores allow you to store and retrieve data from a key-value store. Datastore behaves like a dictionary and you can store and retrieve data from it. Currently, you have three datastores that you can use:

- **local** - data will be stored in the user's browser
- **project** - data will be stored in the project storage
- **account** - data will be stored in your pyscript account storage

This is useful for storing data that you want to persist across multiple runs of your pyscript app or shared data between numerous pyscript apps.

### Using datastores

You can import `datastore` from the `pyscript_dot_com` package in your pyscript app and use it to store and retrieve data:

```python

from pyscript_dot_com import local, project, account

# Store data in the browser
local.datastore['name'] = 'John Doe'

# Store data in the project storage
project.datastore['project-name'] = "my-project"

# Store data in the account storage
if not account.datastore.get("my-project-views"):
    account.datastore["my-project-views"] = 0
account.datastore["my-project-views"] += 1

# We can't access the project datastore from the account
project_name = account.datastore.get("project-name")
assert project_name is None

```

If you are curious to see how you can use both proxies and datastores, you can check this [pyscript module example](https://pyscript.com/@fabiorosado/pyscript-module/latest).
