# Install
```shell script
pip install -U namekox-polycom
```

# Example
> ping.py
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


from namekox_webserver.core.entrypoints.app import app
from namekox_webserver.core.request import JsonRequest
from namekox_polycom.core.dependencies import PolycomHelper


class Ping(object):
    name = 'ping'

    polycom = PolycomHelper()

    @app.api('/api/ping/', methods=['POST'])
    def ping(self, request):
        request = JsonRequest(request)
        request.is_valid(raise_exception=True)
        host = request.json.get('host', '127.0.0.1')
        username = request.json.get('username', 'admin')
        password = request.json.get('password', 'admin')
        self.polycom.add_conn(host, host=host, username=username, password=password)
        return self.polycom.cmd_exec(host, 'ping')
```

# Running
> config.yaml
```yaml
WEBSERVER:
  host: 0.0.0.0
  port: 80
POLYCOM:
  timeout: 15
  bshell_prompt: '->'
  stdout_prompt: "\r\r\n"
  stdout_linsep: "\r\r\n"
  passwd_prompt: "password:"
  finger_prompt: "Are you sure you want to continue connecting"
```
> namekox run ping
```shell script
2021-03-05 09:46:04,876 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2021-03-05 09:46:04,876 DEBUG starting services ['ping']
2021-03-05 09:46:04,877 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2021-03-05 09:46:04,880 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2021-03-05 09:46:04,881 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2021-03-05 09:46:04,881 DEBUG starting service ping dependencies [ping:namekox_polycom.core.dependencies.PolycomHelper:polycom]
2021-03-05 09:46:04,881 DEBUG service ping dependencies [ping:namekox_polycom.core.dependencies.PolycomHelper:polycom] started
2021-03-05 09:46:04,882 DEBUG services ['ping'] started
2021-03-05 09:46:11,620 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x102950310>, ('127.0.0.1', 60742)), kwargs={}, tid=handle_request)
2021-03-05 09:46:11,624 DEBUG spawn worker thread handle ping:ping(args=(<Request 'http://127.0.0.1/api/ping/' [POST]>,), kwargs={}, context={})
2021-03-05 09:46:12,864 DEBUG login 10.10.10.10 success
127.0.0.1 - - [05/Mar/2021 09:46:12] "POST /api/ping/ HTTP/1.1" 200 290 1.353687
2021-03-05 09:46:33,430 DEBUG spawn worker thread handle ping:ping(args=(<Request 'http://127.0.0.1/api/ping/' [POST]>,), kwargs={}, context={})
127.0.0.1 - - [05/Mar/2021 09:46:33] "POST /api/ping/ HTTP/1.1" 200 290 0.114395
^C2021-03-05 09:46:42,165 DEBUG stopping services ['ping']
2021-03-05 09:46:42,167 DEBUG stopping service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2021-03-05 09:46:42,168 DEBUG wait service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stop
2021-03-05 09:46:42,169 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stopped
2021-03-05 09:46:42,170 DEBUG stopping service ping dependencies [ping:namekox_polycom.core.dependencies.PolycomHelper:polycom]
2021-03-05 09:46:42,274 DEBUG service ping dependencies [ping:namekox_polycom.core.dependencies.PolycomHelper:polycom] stopped
2021-03-05 09:46:42,275 DEBUG services ['ping'] stopped
2021-03-05 09:46:42,275 DEBUG killing services ['ping']
2021-03-05 09:46:42,276 DEBUG service ping already stopped
2021-03-05 09:46:42,276 DEBUG services ['ping'] killed
```
> curl -H "Content-Type:application/json" -H "Data_Type:msg" -X POST --data '{"host": "10.10.10.10","username": "admin","password": "admin"}' http://127.0.0.1/api/ping/
```json5
{
    "errs": "",
    "code": "Request:Success",
    "data": {
        "after": [
            "->"
        ],
        "before": [
            "error: command not found"
        ]
    },
    "call_id": "9f8643ee-325f-4c37-a86c-fe860118c5f2"
}
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_polycom.cli.subctx.polycom:Polycom
WEBSERVER:
  host: 0.0.0.0
  port: 80
POLYCOM:
  timeout: 15
  bshell_prompt: '->'
  stdout_prompt: "\r\r\n"
  stdout_linsep: "\r\r\n"
  passwd_prompt: "password:"
  finger_prompt: "Are you sure you want to continue connecting"
```
> namekox shell
```shell script
Namekox Python 2.7.16 (default, Jun  5 2020, 22:59:21)
[GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc- shell on darwin
In [1]: nx.polycom.proxy('10.10.10.10', host='10.10.10.10', username='admin', password='admin').execute('status')
-> Out[1]:
{u'after': [u'->'],
 u'before': [u'inacall offline',
  u'autoanswerp2p online',
  u'remotecontrol online',
  u'microphones online',
  u'visualboard offline',
  u'globaldirectory online',
  u'presenceservice online',
  u'ipnetwork online',
  u'gatekeeper online',
  u'sipserver online',
  u'logthreshold offline',
  u'meetingpassword offline',
  u'provisioning online',
  u'rpms offline',
  u'modularroom offline',
  u'status end']}
```
