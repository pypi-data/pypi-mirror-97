# Install
```shell script
pip install -U namekox-ldap
```


# Example
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


from namekox_ldap.core.dependencies import LdapHelper
from namekox_webserver.core.entrypoints.app import app


class Ping(object):
    name = 'ping'

    # https://ldap3.readthedocs.io/en/latest/
    ldap = LdapHelper(name)

    @app.api('/api/who/am/i/', methods=['GET'])
    def who_am_i(self, request):
        return self.ldap.acquire().extend.standard.who_am_i()
```

# Running
> config.yaml
```yaml
LDAP:
  ping:
    servers:
      - host: ldaps://*.*.*.*:636
      - host: ldaps://*.*.*.*:636
    usrname: namekox
    usrpass: *
    base_dc: cn
    base_dn: *
    retries: 2
```
> namekox run ping
```shell script
2020-11-20 14:45:03,619 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-20 14:45:03,620 DEBUG starting services ['ping']
2020-11-20 14:45:03,621 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:who_am_i, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-11-20 14:45:03,623 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-11-20 14:45:03,623 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:who_am_i, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2020-11-20 14:45:03,623 DEBUG starting service ping dependencies [ping:namekox_ldap.core.dependencies.LdapHelper:ldap]
2020-11-20 14:45:03,624 DEBUG service ping dependencies [ping:namekox_ldap.core.dependencies.LdapHelper:ldap] started
2020-11-20 14:45:03,624 DEBUG services ['ping'] started
2020-11-20 14:45:05,651 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10d357f10>, ('127.0.0.1', 49896)), kwargs={}, tid=handle_request)
2020-11-20 14:45:05,653 DEBUG spawn worker thread handle ping:who_am_i(args=(<Request 'http://127.0.0.1/api/who/am/i/' [GET]>,), kwargs={}, context={})
127.0.0.1 - - [20/Nov/2020 14:45:05] "GET /api/who/am/i/ HTTP/1.1" 200 247 0.226278
```
> curl http://127.0.0.1/api/who/am/i/
```json
{
    "errs": "",
    "code": "Request:Success",
    "data": "u:CN\\namekox",
    "call_id": "ef5a4c26-5eb1-4f71-92a7-962f4596c063"
}
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_ldap.cli.subctx.ldap:Ldap
LDAP:
  ping:
    servers:
      - host: ldaps://*.*.*.*:636
      - host: ldaps://*.*.*.*:636
    usrname: namekox
    usrpass: *
    base_dc: cn
    base_dn: *
    retries: 2
```
> namekox shell
```shell script
Namekox Python 2.7.16 (default, Dec 13 2019, 18:00:32)
[GCC 4.2.1 Compatible Apple LLVM 11.0.0 (clang-1100.0.32.4) (-macos10.15-objc-s shell on darwin
In [1]: nx.ldap.proxy('ping').acquire().extend.standard.who_am_i()
Out[1]: u'u:CN\\namekox'
```
