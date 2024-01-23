from datasette import hookimpl, Response
import httpx


@hookimpl
def register_routes(datasette):
    config = datasette.plugin_config("datasette-proxy-url") or {}
    routes = []
    for path in config.get("paths", []):
        routes.append((path["path"], make_proxy(path["backend"])))
    return tuple(routes)


def make_proxy(url):
    async def proxy(request):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        return Response(response.content, content_type=response.headers["content-type"])

    return proxy
