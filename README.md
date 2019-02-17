google-python-sdk
===================
#### Python - Google API

**google-python-sdk** is a simple client for google api.

## Installation
``` 
sudo pip install google-python-sdk
```

## Using
```python
from google import API
api = API('CLIENT_ID', 'CLIENT_SECRET', 'API_KEY', 'ACCESS_TOKEN')
```

## References https://www.googleapis.com/oauth2/v3/userinfo
```python
profile = api.get_profile()
```

## References https://oauth2.googleapis.com/tokeninfo
```python
tokeninfo = api.get_token_info()
```


## Contributing
[https://github.com/rohitkhatri/google-python-sdk](https://github.com/rohitkhatri/google-python-sdk)