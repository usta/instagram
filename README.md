# instagram
instagram bot to learn

[![Licence](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/hakancelik96/instagram/blob/master/LICENSE.txt)

before
---
- pip install -r requirements.txt

Use as follows
-------

```python
>>> from instagram import Instagram as I
>>> I = I("username", "password")
# if you want to use proxy I("username", "password", True)
>>> I.username
username
>>> I.password
password
>>> I.useragent
# gives random useragent
>>> I.s
# gives requests session
>>> I.s.proxies
# you gives fake proxy ex: 165.321.51.21:8050
>>> I.login() # to login instagram
{'authenticated': True, 'user': True, 'status': 'ok'}
>>> I.logout() # to logout instagram
>>> I.isloggedin  # To check whether loggedin or not
False # or True
>>> I.follow(follow_id = 3) # for @kevin
{'result': 'following', 'status': 'ok'}
>>> I.unfollow(unfollow_id = 3) # for #kevin
{'status': 'ok'}
>>> I.signup(first_name="first_name",email="email") # to signup for instagram
```
