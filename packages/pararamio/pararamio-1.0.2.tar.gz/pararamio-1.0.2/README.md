Setup
-----

Setup package

    # python setup.py install

Examples
--------
```python
import pararamio
client = pararamio.Pararamio('username', 'passowrd', 'two_factor_key')
client.authenticate()
ua = client.search_user('recipient@example.com')
if len(ua) == 1:
    ua[0].send_message(text='text message')
```
