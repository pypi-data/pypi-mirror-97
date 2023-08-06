Deployment
==========

Depending on your setup and preferences, there are multiple ways to run Emmett applications. In this chapter, we'll try to document the most common ones.

If you want to use an ASGI server not listed in this section, please refer to its documentation, remembering that your Emmett application object is the actual ASGI application (following spec version 3.0).

Included server
---------------

*Changed in version 2.2*

Emmett comes with an included server based on [uvicorn](https://www.uvicorn.org/). In order to run your application in production you can just use the included `serve` command:

    emmett serve --host 0.0.0.0 --port 80

You can inspect all the available options of the `serve` command using the `--help` option. Here is the full list:

| option | default | description |
| --- | --- | --- |
| host | 0.0.0.0 | Bind address |
| port | 8000 | Bind port |
| workers | 1 | Number of worker processes | 
| loop | auto | Loop implementation (possible values: auto,asyncio,uvloop) |
| http-protocol | auto | HTTP protocol implementation (possible values: auto,h11,httptools) |
| ws-protocol | auto | Websocket protocol implementation (possible values: auto,websockets,wsproto) |
| log-level | info | Logging level (possible values: debug,info,warning,error,critical) |
| access-log | (flag) enabled | Enable/disable access log |
| proxy-headers | (flag) disabled | Enable/disable proxy headers |
| proxy-trust-ips | | Comma separated list of IPs to trust for proxy headers |
| max-concurrency | | Limit number of concurrent connections |
| backlog | 2048 | Maximum connection queue |
| keep-alive-timeout | 0 | Connection keep-alive timeout |
| ssl-certfile | | Path to SSL certificate file |
| ssl-keyfile | | Path to SSL key file |
| ssl-cert-reqs | | SSL client certificate requirements (see `ssl` module) |
| ssl-ca-certs | | SSL CA allowed certificates |

Gunicorn
--------

The included server might suit most of the common demands, but whenever you need a fully featured server, you can use [Gunicorn](https://gunicorn.org).

Emmett includes a Gunicorn worker class allowing you to run ASGI applications with the Emmett's environment, while also giving you Gunicorn's fully-featured process management:

    gunicorn myapp:app -w 4 -k emmett.asgi.workers.EmmettWorker

This allows you to increase or decrease the number of worker processes on the fly, restart worker processes gracefully, or perform server upgrades without downtime.

Docker
------

Even if Docker is not properly a deployment option, we think giving an example of a `Dockerfile` for an Emmett application is proficient for deployment solutions using container orchestrators, such as Kubernetes or Mesos.

In order to keep the image lighter, we suggest to use the *slim* Python image as a source:

```Dockerfile
FROM python:3.9-slim

RUN mkdir -p /usr/src/deps
COPY requirements.txt /usr/src/deps

WORKDIR /usr/src/deps
RUN pip install --no-cache-dir -r /usr/src/deps/requirements.txt

COPY ./ /app
WORKDIR /app

EXPOSE 8000

CMD [ "emmett", "serve" ]
```
