# Install
```shell script
pip install -U namekox-config
```

# Example
> ping.py
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


from namekox_webserver.core.entrypoints.app import app
from namekox_config.core.dependencies import ConfigHelper


class Ping(object):
    name = 'ping'

    cfg = ConfigHelper()

    @app.api('/api/config/', methods=['GET'])
    def config(self, request):
        return self.cfg
```

# Running
> config.yaml
```yaml
WEBSERVER:
  host: 0.0.0.0
  port: 80
```
> namekox run ping
```shell script
2020-12-01 15:43:34,009 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-12-01 15:43:34,010 DEBUG starting services ['ping']
2020-12-01 15:43:34,010 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:config, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-12-01 15:43:34,012 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-12-01 15:43:34,012 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:config, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2020-12-01 15:43:34,012 DEBUG starting service ping dependencies [ping:namekox_config.core.dependencies.ConfigHelper:cfg]
2020-12-01 15:43:34,013 DEBUG service ping dependencies [ping:namekox_config.core.dependencies.ConfigHelper:cfg] started
2020-12-01 15:43:34,013 DEBUG services ['ping'] started
2020-12-01 15:43:36,030 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10fb95890>, ('127.0.0.1', 56088)), kwargs={}, tid=handle_request)
127.0.0.1 - - [01/Dec/2020 15:43:36] "GET /api/config HTTP/1.1" 308 460 0.001316
2020-12-01 15:43:36,039 DEBUG spawn worker thread handle ping:config(args=(<Request 'http://127.0.0.1/api/config/' [GET]>,), kwargs={}, config={})
127.0.0.1 - - [01/Dec/2020 15:43:36] "GET /api/config/ HTTP/1.1" 200 279 0.000898
^C2020-12-01 15:43:37,886 DEBUG stopping services ['ping']
2020-12-01 15:43:37,887 DEBUG stopping service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:config, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-12-01 15:43:37,888 DEBUG wait service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:config, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stop
2020-12-01 15:43:37,888 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:config, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stopped
2020-12-01 15:43:37,888 DEBUG stopping service ping dependencies [ping:namekox_config.core.dependencies.ConfigHelper:cfg]
2020-12-01 15:43:37,888 DEBUG service ping dependencies [ping:namekox_config.core.dependencies.ConfigHelper:cfg] stopped
2020-12-01 15:43:37,889 DEBUG services ['ping'] stopped
2020-12-01 15:43:37,889 DEBUG killing services ['ping']
2020-12-01 15:43:37,889 DEBUG service ping already stopped
2020-12-01 15:43:37,889 DEBUG services ['ping'] killed
```
> curl http://127.0.0.1/api/config/
```json
{
    "errs": "",
    "code": "Request:Success",
    "data": {
        "WEBSERVER": {
            "host": "0.0.0.0",
            "port": 80
        }
    },
    "call_id": "8b309176-e0e1-492d-aaf6-a060888e96a5"
}
```
