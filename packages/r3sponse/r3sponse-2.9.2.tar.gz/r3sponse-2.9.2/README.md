# r3sponse
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: macos & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"> 
</p>

## Table of content:
  * [Description](#description)
  * [Installation](#installation)
  * [Code Examples](#code-examples)

# Description:
Some description.

# Installation:
Install the package.

	curl -s https://raw.githubusercontent.com/vandenberghinc/r3sponse/master/r3sponse/requirements/installer.remote | bash 

## Example Function.
An example function that returns a ResponseObject class.

```python

# import the package
from r3sponse import r3sponse

# universal responses.
def my_function():

	# return an error response from a function.
	return r3sponse.error("Failed to retrieve your personal API key")

	# return a success response from a function.
	return r3sponse.success("Success retrieved your personal API key", {
		"api_key":api_key,
	})

# check if a response was successfull.
response = my_function()
if response.success:
	message = response["message"]
else:
	error = response["error"]

```

# Code Examples:

### Table of content:
- [__Parameters__](#parameters)
  * [get](#get)
  * [check](#check)
- [__R3sponse__](#r3sponse)
  * [success](#success)
  * [error](#error)
  * [log](#log)
  * [load_logs](#load_logs)
  * [reset_logs](#reset_logs)
  * [serialize](#serialize)
  * [response](#response)
- [__ResponseObject__](#responseobject)
  * [clean](#clean)
  * [assign](#assign)
  * [crash](#crash)
  * [unpack](#unpack)
  * [remove](#remove)
  * [iterate](#iterate)
  * [items](#items)
  * [keys](#keys)
  * [values](#values)
  * [reversed](#reversed)
  * [sort](#sort)
  * [dict](#dict)
  * [json](#json)
  * [serialize](#serialize-1)
  * [instance](#instance)
  * [raw](#raw)

## Parameters:
The parameters object class.
``` python 

# initialize the parameters object class.
parameters = Parameters()

```

#### Functions:

##### get:
``` python

# call parameters.get.
_ = parameters.get(
    # the django request (1).
    request=None,
    # the identifiers (#2).
    #    str instance: return the parameters value.
    #    list instance: return a parameters object & return an error response when a parameter is undefined.
    #    dict instance: return a parameters object & return the parameter's value from the dict as a default when undefined.
    parameters=[],
    # default return value (dict instance of parameters overwrites the default parameter).
    default=None,
    # traceback id.
    traceback=None, )

```
##### check:
``` python

# call parameters.check.
response = parameters.check(
    # the parameters (dict) (#1).
    parameters={"parameter":None},
    # the recognizer value for when the parameters are supposed to be empty.
    default=None,
    # the traceback id.
    traceback=None, )

```

## R3sponse:
The r3sponse object class.
``` python 

# import the r3sponse object class.
from r3sponse import r3sponse

```

#### Functions:

##### success:
``` python

# call r3sponse.success.
_ = r3sponse.success(
    # the message (must be param #1).
    message,
    # additional returnable functions (must be param #2).
    variables={},
    # log log level of the message (int).
    log_level=None,
    # the required log level for when printed to console (leave None to use r3sponse.log_level).
    required_log_level=None,
    # save the error to the logs file.
    save=False,
    # return as a django JsonResponse.
    django=False, )

```
##### error:
``` python

# call r3sponse.error.
_ = r3sponse.error(
    # the error message.
    error="",
    # log log level of the message (int).
    log_level=None,
    # the required log level for when printed to console (leave None to use r3sponse.log_level).
    required_log_level=None,
    # save the error to the erros file.
    save=False,
    # return as a django JsonResponse.
    django=False,
    # raise error for developer traceback.
    traceback=ERROR_TRACEBACK, )

```
##### log:
``` python

# call r3sponse.log.
_ = r3sponse.log(
    # option 1:
    # the message (#1 param).
    message=None,
    # option 2:
    # the error.
    error=None,
    # option 3:
    # the response dict (leave message None to use).
    response={},
    # print the response as json.
    json=False,
    # optionals:
    # the log level for printing to console.
    log_level=0,
    # the required log level for when printed to console (leave None to use r3sponse.log_level).
    required_log_level=None,
    # save to log file.
    save=False,
    # save errors only (for option 2 only).
    save_errors=False, )

```
##### load_logs:
``` python

# call r3sponse.load_logs.
_ = r3sponse.load_logs(format="webserver", options=["webserver", "cli", "array", "string"])

```
##### reset_logs:
``` python

# call r3sponse.reset_logs.
_ = r3sponse.reset_logs()

```
##### serialize:
``` python

# call r3sponse.serialize.
_ = r3sponse.serialize(response={})

```
##### response:
``` python

# call r3sponse.response.
_ = r3sponse.response(
    # the blank response (dict) (#1).
    response={
        "success":False,
        "message":None,
        "error":None,
    },
    # the safe boolean (serialize from dumped json).
    safe=False, )

```

## ResponseObject:
The response_object object class.
``` python 

# initialize the response_object object class.
response_object = ResponseObject(
    # the response attributes.
    attributes={
        "success":False,
        "message":None,
        "error":None,
    },
    # import a dumped json response (str) (ignores attributes).
    json=None, )

```

#### Functions:

##### clean:
``` python

# call response_object.clean.
_ = response_object.clean()

```
##### assign:
``` python

# call response_object.assign.
_ = response_object.assign(dictionary)

```
##### crash:
``` python

# call response_object.crash.
_ = response_object.crash(error="ValueError", traceback=True, json=False)

```
##### unpack:
``` python

# call response_object.unpack.
_ = response_object.unpack(
    # the key / keys / defaults parameter (#1).
    # str instance:
    #   unpack the str key
    # list instance:
    #   unpack all keys in the list.
    # dict instance:
    #   unpack all keys from the dict & when not present return the key's value as default.
    keys, )

```
##### remove:
``` python

# call response_object.remove.
_ = response_object.remove(keys=[], values=[], save=False)

```
##### iterate:
``` python

# call response_object.iterate.
_ = response_object.iterate(sorted=False, reversed=False)

```
##### items:
``` python

# call response_object.items.
_ = response_object.items(sorted=False, reversed=False, dictionary=None)

```
##### keys:
``` python

# call response_object.keys.
_ = response_object.keys(sorted=False, reversed=False)

```
##### values:
``` python

# call response_object.values.
_ = response_object.values(sorted=False, reversed=False, dictionary=None)

```
##### reversed:
``` python

# call response_object.reversed.
_ = response_object.reversed(dictionary=None)

```
##### sort:
``` python

# call response_object.sort.
_ = response_object.sort(alphabetical=True, ascending=False, reversed=False, dictionary=None)

```
##### dict:
``` python

# call response_object.dict.
_ = response_object.dict(sorted=False, reversed=False, json=False)

```
##### json:
``` python

# call response_object.json.
_ = response_object.json(sorted=False, reversed=False, indent=4, dictionary=None, )

```
##### serialize:
``` python

# call response_object.serialize.
_ = response_object.serialize(sorted=False, reversed=False, json=False, dictionary=None)

```
##### instance:
``` python

# call response_object.instance.
_ = response_object.instance()

```
##### raw:
``` python

# call response_object.raw.
_ = response_object.raw()

```

