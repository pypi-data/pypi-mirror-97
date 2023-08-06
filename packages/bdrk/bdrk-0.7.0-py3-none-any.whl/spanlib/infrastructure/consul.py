import asyncio
import ssl

import aiohttp
import consul.aio
import consul.base

HTTP_SCHEME = "http"
HTTPS_SCHEME = "https"


def get_scheme(use_ssl: bool):
    return HTTPS_SCHEME if use_ssl else HTTP_SCHEME


class PatchedHTTPClient(consul.aio.HTTPClient):
    """Patches py-consul to fix unused self.cert.

    Adapted from: https://github.com/criteo-forks/py-consul/blob/v1.2.1/consul/aio.py
    """

    def __init__(
        self, *args, loop=None, connections_limit=None, connections_timeout=None, **kwargs
    ):
        # Skip init of consul.aio.HTTPClient
        consul.base.HTTPClient.__init__(self, *args, **kwargs)
        self._loop = loop or asyncio.get_event_loop()

        connector_kwargs = {
            "ssl": ssl.create_default_context(cafile=self.cert) if self.verify else False
        }  # Patched
        if connections_limit:
            connector_kwargs["limit"] = connections_limit
        connector = aiohttp.TCPConnector(loop=self._loop, **connector_kwargs)

        session_kwargs = {}
        if connections_timeout:
            timeout = aiohttp.ClientTimeout(total=connections_timeout)
            session_kwargs["timeout"] = timeout

        self._session = aiohttp.ClientSession(connector=connector, **session_kwargs)

    async def _request(self, callback, method, uri, data=None):
        async with self._session.request(method, uri, data=data) as resp:  # Patched
            body = await resp.text(encoding="utf-8")
            if resp.status == 599:
                raise consul.base.Timeout
            r = consul.base.Response(resp.status, resp.headers, body)
            return callback(r)


class PatchedConsul(consul.aio.Consul):
    """Patches py-consul to fix unused `cert` param.

    Adapted from: https://github.com/criteo-forks/py-consul/blob/v1.2.1/consul/aio.py
    """

    def http_connect(self, host, port, scheme, verify=True, cert=None):
        return PatchedHTTPClient(
            host,
            port,
            scheme,
            loop=self._loop,
            connections_limit=self.connections_limit,
            connections_timeout=self.connections_timeout,
            verify=verify,
            cert=cert,
        )  # Patched
