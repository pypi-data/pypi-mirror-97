# NetManager
- Version: 2.1 (05.03.21)
- Author: Danila Kisluk
- VK: https://vk.com/danilakisluk
- Gmail: dankis12a@gmail.com


## Installation
`pip install netmamanger`


## Description
NetManager is a Python library for interacting with the Internet from Kivy Android apps.
You can also use NetManager for interacting with the Internet from other projects.
NetManger can make network requests and interact with Firebase Realtime Database.


## What's new in version 2.1?
- Added description.
- Fixed small bugs.


## NetRequest
NetRequest makes network requests and returns their results.
```python
from netmanager import NetRequest


url = "some.url/path"
# Writing 'https://' is optional. This does not apply to other protocols.


""" GET request """
get_request = NetRequest(url)
# 'GET' is default method.

status = get_request.status
headers = get_request.headers
result = get_request.result

print(status, type(status))
# 200 <class 'int'>

print(headers, type(headers))
# {"header": "header_data"} <class 'dict'>

print(result, type(result))
# {"response":"response_data"} <class 'str'>


""" POST request """
post_request = NetRequest(url, method='POST', data='{"key":"value"}')

status = post_request.status
headers = post_request.headers
result = post_request.result

print(status, type(status))
# 200 <class 'int'>

print(headers, type(headers))
# {'header': 'header_data'} <class 'dict'>

print(result, type(result))
# {"response":"response_data"} <class 'str'>
```


## FirebaseRTDB
FirebaseRTDB interact with Firebase Realtime Database.
```python
from netmanager import FirebaseRTDB


database_url = "my-default-rtdb.firebasedatabase.app"
# Writing 'https://' is optional. This does not apply to other protocols.

db = FirebaseRTDB(database_url)
path = "users"
# '/' is default path.


""" Get """
users = db.get(path)
print(users, type(users))
# {"user1":"user_data"} <class 'str'>


""" Set """
data = '{"user1":"new_user_data"}'
set = db.set(path, data)
print(set, type(set))
# 200 <class 'int'>
```
